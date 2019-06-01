from django.core.cache import cache
from django.db.models import Sum

from java_wallet.models import Account, Transaction, RewardRecipAssign, Block, Asset
from scan.models import MultiOut


def get_account_name(account_id: int) -> str:
    key = "account_name:{}".format(account_id)

    account_name = cache.get(key)

    if account_name is None:
        account_name = Account.objects.using('java-wallet').filter(
            id=account_id, latest=True
        ).values_list(
            'name', flat=True
        ).first()
        cache.set(key, account_name or '')

    return account_name


def get_asset_name(asset_id: int) -> str:
    key = "asset_name:{}".format(asset_id)

    asset_name = cache.get(key)

    if asset_name is None:
        asset_name = Asset.objects.using('java-wallet').filter(
            id=asset_id
        ).values_list(
            'name', flat=True
        ).first()
        cache.set(key, asset_name or '')

    return asset_name


def get_txs_count_in_block(block_id: int) -> int:
    key = "block_txs_count:{}".format(block_id)

    cnt = cache.get(key)

    if cnt is None:
        cnt = Transaction.objects.using('java-wallet').filter(block_id=block_id).count()
        cache.set(key, cnt)

    return cnt


def get_pool_id_for_block(block: Block) -> int:
    key = "block_pool:{}".format(block.id)

    recipient_id = cache.get(key, -1)

    if recipient_id == -1:
        recipient_id = Transaction.objects.using('java-wallet').filter(
            type=20,
            height__lte=block.height,
            sender_id=block.generator_id
        ).values_list(
            'recipient_id', flat=True
        ).order_by('-height').first()

        cache.set(key, recipient_id)

    return recipient_id


def get_pool_id_for_account(address_id: int) -> int:
    key = "block_pool:{}".format(address_id)

    pool_id = cache.get(key, -1)

    if pool_id == -1:
        pool_id = RewardRecipAssign.objects.using('java-wallet').filter(
            account_id=address_id
        ).values_list(
            'recip_id', flat=True
        ).order_by(
            '-height'
        ).first()

        cache.set(key, pool_id)

    return pool_id


def get_all_burst_amount() -> int:
    key = "all_burst_amount"

    amount = cache.get(key)

    if amount is None:
        amount = Account.objects.using('java-wallet').filter(
            latest=True
        ).aggregate(Sum('balance'))['balance__sum']

        cache.set(key, amount, 86400)

    return amount


def get_txs_count() -> int:
    key = "txs_count"

    amount = cache.get(key)

    if amount is None:
        amount = Transaction.objects.using('java-wallet').count()
        cache.set(key, amount, 3600)

    return amount


def get_multiouts_count() -> int:
    key = "multiouts_count"

    amount = cache.get(key)

    if amount is None:
        amount = MultiOut.objects.count()
        cache.set(key, amount, 3600)

    return amount


def get_last_height() -> int:
    key = "last_height"

    height = cache.get(key)

    if height is None:
        height = Block.objects.using('java-wallet').order_by(
            '-height'
        ).values_list(
            'height', flat=True
        ).first()
        cache.set(key, height, 10)

    return height
