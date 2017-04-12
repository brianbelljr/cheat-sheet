


def process_pull_request(data):
    if data['action'] in ["assigned", "unassigned", "review_requested", "review_request_removed", "labeled", "unlabeled", "opened", "edited", "closed", "reopened"]:
        return data['action']
    #if data['action'] == 'labeled':
    #    reviews.process_pr_labeled(data)
    #elif data['action'] == 'closed':
    #    reviews.process_pr_closed(data)
    # elif data['action'] == 'opened':
    #     github_jira.process_pr_opened(data)
    # elif data['action'] == 'edited':
    #     github_jira.process_pr_edited(data)
