import os
import sys
import django
import celery

import test_settings

BASE_PATH = os.path.dirname(__file__)


def main():
    """
    Standalone django model test with a 'memory-only-django-installation'.
    You can play with a django model without a complete django app installation.
    http://www.djangosnippets.org/snippets/1044/
    """

    # Django標準のdjango.conf.global_settingsを設定してしまうと、
    # Django3では、global_settingsの全ての定数を上書きする挙動になってしまい、
    # Django3の仕様で、多重上書き禁止エラーが検知され、例外が発生する。
    # (例) https://github.com/django/django/blob/70035fb0444ae7c01613374212ca5e3c27c9782c/django/conf/__init__.py#L188
    # そのため、自前のテスト用settingsモジュール(test_settings.py)を設定する。
    os.environ["DJANGO_SETTINGS_MODULE"] = "test_settings"

    app = celery.Celery()
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.autodiscover_tasks(lambda: test_settings.INSTALLED_APPS)

    django.setup()

    from django.test.utils import get_runner

    # test用のsettings情報を用いて、Djangoのtest runnerクラスを取得
    TestRunner = get_runner(test_settings)

    # test runnerオブジェクトを生成
    test_runner = TestRunner()

    # test runnerにbpmailerの単体テストのPathを渡して、bpmailerの単体テストを実行する
    failures = test_runner.run_tests(['beproud.django.notify.tests'])

    sys.exit(failures)


if __name__ == '__main__':
    main()
