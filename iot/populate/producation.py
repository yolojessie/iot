from populate import base
from populate import address
from account.models import User

address.populate()
print('Creating admin account ... ', end='')
User.objects.create_superuser(username='admin', password='jj840904', email=None, fullName='管理者')
print('done')