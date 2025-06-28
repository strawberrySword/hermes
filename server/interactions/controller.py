import interactions.service as service
from __main__ import app

from auth.service import auth_required


@app.route('/api/interactions/<article_id>', methods=['POST'])
@auth_required
def open_article(user_email, article_id):
    service.record_opened(user_email, article_id)
    return 'article opened', 201
