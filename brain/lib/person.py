import json
from paranuara.models import Company, Person
from wstypes.error import Error, NoResultsError
from wstypes.person import WSPerson
from wstypes.wslist import List
from django.db.models.query import QuerySet

class PersonTable(object):
    """
    Class representing an abstraction of the Company database table.
    """

    def to_ws_person(self, person, get_food=False, basic_info=False,
                     all_info=True, username=False, age=False):
        """
        Convert the provided person db object into a wstype.

        :param person: The person db object.
        :type person: Person
        :param get_food: Return food and vegetables that person like if True.
        :type get_food: bool
        :param basic_info: Return person's name, address, age and phone info if True.
        :type basic_info: bool
        :param all_info: Return all info for person if True.
        :type all_info: bool
        :param username: Return person's username if True.
        :type username: bool
        :param age: Return person's age if True.
        :type age: bool
        :return: WS type for the person db object
        :rtype: WSPerson
        """
        try:
            attr = {}

            # Attempt to get vegetables & fruits for the person
            if get_food or all_info:
                try:
                    attr['vegetables'] = json.loads(person.vegetables)
                except Exception, e:
                    print "Error: Failed to get vegetables for " \
                          "user %s: %s" % (attr.get('username'), e)

                try:
                    attr['fruits'] = json.loads(person.fruits)
                except Exception, e:
                    print "Error: Failed to get fruits for " \
                          "user %s: %s" % (attr.get('username'), e)

            # Return username
            if username or all_info:
                attr['username'] = getattr(person, 'username', None)

            # Return age for basic and all info as well as if age is set to True
            if age or basic_info or all_info:
                attr['age'] = getattr(person, 'age', None)

            # Return basic info
            if basic_info or all_info:
                attr.update({
                    'name': getattr(person, 'name', None),
                    'address': getattr(person, 'address', None),
                    'phone': getattr(person, 'phone', None)
                })

            # Return all the information
            if all_info:
                # Attempt to get the company name for the person
                company = getattr(person, 'company', None)
                if company:
                    company = getattr(company, 'name', None)

                attr.update({
                    'died': getattr(person, 'died', None),
                    'balance': getattr(person, 'balance', None),
                    'picture': getattr(person, 'picture', None),
                    'eye_color': getattr(person, 'eye_color', None),
                    'gender': getattr(person, 'gender', None),
                    'email': getattr(person, 'email', None),
                    'description': getattr(person, 'description', None),
                    'registered_date': getattr(person, 'registered_date', None),
                    'tags': getattr(person, 'tags', None),
                    'company': company
                })

            return WSPerson(**attr)
        except Exception, e:
            error_msg = "Error: Failed to convert Person DB to WSPerson: %s" % e
            print error_msg
            return NoResultsError(message=error_msg)

    def get_by_username(self, username):
        """
        Get basic info - username, age and fav fruits and vegetables that user
        likes.

        :param username: Username of the person whose details are required.
        :type username: str
        :return: Person info if found.
        :rtype: WSPerson or Error
        """
        error_msg = None
        try:
            person = Person.objects.filter(username__exact=username)
            if isinstance(person, QuerySet) and person.count():
                return self.to_ws_person(person[0], all_info=False,
                                         username=True, age=True, get_food=True)
        except Exception, e:
            error_msg = "Error: Failed to retrieve person by " \
                        "username %s: %s" % (username, e)
            print error_msg
        return NoResultsError(message=error_msg)

    def get_by_company(self, company_name=None):
        """
        Get list of person by company.

        :param company_name: The company name whose employees needs to be
        returned.
        :type company_name: str
        :return: List of employees if found.
        :rtype: WSList or Error
        """
        try:
            # Retrieve company and if not found then return an error
            company = Company.objects.filter(name__exact=company_name)
            if isinstance(company, QuerySet) and company.count():
                company = company[0]
            if not company:
                error_msg = "Error: Company not found by name %s" % company_name
                return NoResultsError(message=error_msg)

            # Retrieve persons based on the company
            employees = Person.objects.filter(company=company)
            if not employees:
                error_msg = "Error: No employees found for %s" % company_name
                return NoResultsError(message=error_msg)

            ws_employees = []
            for employee in employees:
                ws_employees.append(self.to_ws_person(employee))
            return List(**{
                'items': ws_employees,
                'description': 'Employees for %s' % company_name
            })
        except Exception, e:
            error_msg = "Error: Failed to retrieve person for " \
                        "company name %s: %s" % (company_name, e)
            print error_msg
        return NoResultsError(message=error_msg)

    def get_common_friends(self, p1_username, p2_username):
        """
        Get p1 and p2 user details along with their common friends who are alive
        and have brown eyes.

        :param p1_username: Username of person 1.
        :type p1_username: str
        :param p2_username: Username of person 2.
        :type p2_username: str
        :return: Json info of person 1 and 2 along with the list of common
        friends who are alive and have brown eyes.
        :rtype: JSON or Error
        """
        try:
            p1 = Person.objects.filter(username__exact=p1_username)
            if isinstance(p1, QuerySet) and p1.count():
                p1 = p1[0]
            else:
                error_msg = "Error: User not found for username: %s" % p1_username
                return NoResultsError(message=error_msg)

            p2 = Person.objects.filter(username__exact=p2_username)
            if isinstance(p2, QuerySet) and p2.count():
                p2 = p2[0]
            else:
                error_msg = "Error: User not found for username: %s" % p2_username
                return NoResultsError(message=error_msg)

            p1_friends = p1.friends.all()
            p2_friends = p2.friends.all()
            common_friends = list(set(p1_friends).intersection(p2_friends))

            # Filter common friends who are not alive and who have brown eyes
            items = []
            for friend in common_friends:
                if friend.died or friend.eye_color != 'brown':
                    continue
                items.append(self.to_ws_person(friend, basic_info=True,
                                               all_info=False))

            # Add details of person 1 and person 2
            resp = {}
            p1_json = self.to_ws_person(p1, basic_info=True,
                                        all_info=False).to_json()
            resp[p1.username] = p1_json['Person']
            p2_json = self.to_ws_person(p2, basic_info=True,
                                        all_info=False).to_json()
            resp[p2.username] = p2_json['Person']

            # Add common friends to response
            common_friends = List(**{
                'items': items,
                'description': 'Common friends of %s and %s who are alive '
                               'and have brown '
                               'eyes' % (p1_username, p2_username),
                'total': len(items)
            }).to_json()
            resp['common_friends'] = common_friends

            return resp
        except Exception, e:
            error_msg = "Error: Failed to retrieve common friends for " \
                        "%s and %s: %s" % (p1_username, p2_username, e)
            print error_msg
        return NoResultsError(message=error_msg)