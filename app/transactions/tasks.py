from __future__ import absolute_import, unicode_literals
from celery import task
from transactions.models import Transaction
from contextlib import contextmanager
from django.core.cache import cache
import time
LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes

@contextmanager
def memcache_lock(lock_id, oid):
    timeout_at = time.monotonic() + LOCK_EXPIRE - 3
    status = cache.add(lock_id, oid, LOCK_EXPIRE)
    try:
        yield status
    finally:
        if time.monotonic() < timeout_at and status:
            cache.delete(lock_id)

@task(bind=True)
def process_transaction(self, transaction_id):
    transaction = Transaction.objects.get(id=int(transaction_id))
    lock_id = f'{transaction.origin.id}-lock-{transaction.coin.id}'
    with memcache_lock(lock_id, self.app.oid) as acquired:
        if acquired:
            transaction.process()
        else:
            self.retry(countdown=10)
