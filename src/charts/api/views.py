from rest_framework.views import APIView
from rest_framework.response import Response
from tickets.models import Ticket

""" 
NOTES TO SELF: 

- highest voted bugs and features - chart with 2 categories containing number of all votes on bugs and features
- number of issues tended to on  a - daily, weekly,  monthly basis
-

"""


def get_data():
    ticketNumbers = Ticket.objects.all().order_by('-votes')
    ticketStatus = Ticket.objects.exclude(status='resolved').order_by('-votes')

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

    for ticket in ticketNumbers:
        if ticket.issue == 'bug':
            data['bug_votes'] += ticket.votes
            data['num_of_bugs'] += 1
            bug = {
                'votes': ticket.votes,
                'title': ticket.issue + ': #' + str(ticket.id),
            }
            data['highest_bugs'].append(bug)
        else:
            data['feature_votes'] += ticket.votes
            data['num_of_features'] += 1
            feature = {
                'votes': ticket.votes,
                'title': ticket.issue + ': #' + str(ticket.id),
            }
            data['highest_features'].append(feature)

        if ticket.status == 'need help':
            data['need_help'] += 1
        elif ticket.status == 'in progress':
            data['in_progress'] += 1
        else:
            data['resolved'] += 1

    for ticket in ticketStatus:
        feature = {
            'title': ticket.issue + ': #' + str(ticket.id),
            'votes': ticket.votes,
            'earned': ticket.earned,
        }
        data['highest_status'].append(feature)

    # sort
    data['highest_bugs'].sort(key=lambda x: x['votes'], reverse=True)
    data['highest_features'].sort(key=lambda x: x['votes'], reverse=True)
    data['highest_status'].sort(key=lambda x: (x['earned'], x['votes']), reverse=True)
    return data


class ChartsAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
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
