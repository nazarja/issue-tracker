from rest_framework.views import APIView
from rest_framework.response import Response
from tickets.models import Ticket


def get_data():
    """
    function to do the heavy lifting, queries Tickets model
    sorts lists and creates new data relevant to display charts data
    """

    # order by votes, exclude resolved as they wont be  tended to anymore
    ticketNumbers = Ticket.objects.all().order_by('-votes')
    ticketStatus = Ticket.objects.exclude(status='resolved').order_by('-votes')

    # json response to send back
    data = {
        'bug_votes': 0,
        'feature_votes': 0,
        'num_of_bugs': 0,
        'num_of_features': 0,
        'need_help': 0,
        'in_progress': 0,
        'resolved': 0,
        'highest_bugs': [],
        'highest_features': [],
        'highest_status': [],
    }

    # gather data - increase values, store in data dict
    for ticket in ticketNumbers:

        # if its a bug
        if ticket.issue == 'bug':
            data['bug_votes'] += ticket.votes
            data['num_of_bugs'] += 1
            bug = {
                'votes': ticket.votes,
                'title': ticket.issue + ': #' + str(ticket.id),
            }
            data['highest_bugs'].append(bug)

        # if its a feature
        else:
            data['feature_votes'] += ticket.votes
            data['num_of_features'] += 1
            feature = {
                'votes': ticket.votes,
                'title': ticket.issue + ': #' + str(ticket.id),
            }
            data['highest_features'].append(feature)

        # tickets which the status of ...
        if ticket.status == 'need help':
            data['need_help'] += 1
        elif ticket.status == 'in progress':
            data['in_progress'] += 1
        else:
            data['resolved'] += 1

    # most tended to data
    for ticket in ticketStatus:
        feature = {
            'title': ticket.issue + ': #' + str(ticket.id),
            'votes': ticket.votes,
            'earned': ticket.earned,
        }
        data['highest_status'].append(feature)

    # sort data by votes
    # most tended to should be sorted by earnings, followed by votes
    data['highest_bugs'].sort(key=lambda x: x['votes'], reverse=True)
    data['highest_features'].sort(key=lambda x: x['votes'], reverse=True)
    data['highest_status'].sort(key=lambda x: (x['earned'], x['votes']), reverse=True)
    return data


class ChartsAPIView(APIView):
    """
    responds to front end get request for charts data
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        """
        respond with response object as json, in some cases,
        we only what the top 10 results from a list, create the array's
        here instead of on the front end.
        """
        data = get_data()
        response = {
            'highestVotes': [data['bug_votes'], data['feature_votes']],
            'numOfTickets': [data['num_of_bugs'], data['num_of_features']],
            'ticketStatus': [data['need_help'], data['in_progress'], data['resolved']],
            'highestBugs':  data['highest_bugs'][:10],
            'highestFeatures':  data['highest_features'][:10],
            'highestStatus':  data['highest_status'][:10],
        }
        return Response(response)
