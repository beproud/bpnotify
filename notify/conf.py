#:coding=utf8:

# NOTICE_TYPESを増やすと、MEDIA_DEFAULTSにも増やさないと通知が来ない
NOTICE_TYPES = (
    ('SIGNUP',  u'会員仮登録完了通知'),
    ('SIGNUP_COMPLETE',  u'会員登録完了通知'),
    ('REMIND_PASSWD',  u'パスワードリマインド'),
    ('INQUIRY',  u'お問い合わせ'),
    ('CHANGE_EMAIL',  u'Eメールアドレス変更通知'),
    ('CHANGE_EMAIL_COMPLETE',  u'Eメールアドレス変更完了通知'),
    
    #(999, '#TODO',  u'要設定メール項目'),

    ### メール受信設定で受信する/しないを選ぶことができる機能
    ('ANSWER_TO_A',  u'回答登録完了'), #回答者向け
    ('ANSWER_TO_F',  u'回答登録完了'), #読者向け
    ('ANSWER_TO_Q',  u'回答通知メール(質問者向け)フォーム'),
    ('SUPPL_ANSWER_TO_Q',  u'回答補足通知メール(質問者向け)フォーム'),
    ('RATING_TO_A',  u'評価通知メール(回答者向け)'),
    ('SUPPL_QUESTION_TO_A' , u'質問補足通知メール（回答者向け)'),
    ('THANKS_TO_A',  u'お礼返信通知メール(回答者向け)'),
    ('THANKSALL_TO_A',  u'みんなへお礼返信通知メール(回答者向け)'),

    ### 絶対に送るメール
    ('REMOVE_QUESTION_TO_Q',  u'質問削除通知メール(質問者向け)'),
    ('RESIGN_COMPLETE',  u'退会通知メール'),
    ('QUESTION',  u'質問登録完了'), #自分向け
    ('QUESTION_TO_F',  u'質問登録完了'), #読者向け
    ('BESTANSWER_TO_A',  u'ベスト回答通知メール(回答者向け)'),
    ('CLOSE_QUESTION_TO_Q',  u'質問終了通知メール(質問者向け)'),
    ('REVISE_MAILADDR',  u'メールアドレス変更受付メール'),
    ('REVISED_MAILADDR',  u'メールアドレス変更完了メール'),

    ('REMIND_RATING' , u'満足設定してくださいアラートメール'),

    # お問い合わせ
    ('INQUIRY',  u'お問い合わせ'), # only mobile
    ('INQUIRY_STAFF',  u'お問い合わせメール(管理向け)'), # only mobile
    ('INQUIRY_POLICE',  u'モバイルお問い合わせメール(警察・教育機関)'), # only mobile

    ('FOLLOW_SUBSCRIBER',  u'読者登録された'), 

    ('EXCHANGE_AMEGOLD',  u'アメゴールド交換申請メール'), 
    ('EXCHANGE_LIFEMILE' , u'ライフマイル交換完了通知メール'),

    #システム管理者向けメール
    ('DAILY_STAT_REPORT',u'デイリーレポート'), # 運営者
    ('BEST_ANS_WARNING_MAIL' , u'自作自演ユーザアラートメール'),
    ('DENY_QUESTION_USER' , u'質問利用不可能通知メール'),
    ('ALERT_QUESTIONAHOLIC' , u'質問中毒者アラートメール'), #運営者向け

    # つぶやき
    ('MURMUR_TO_SELF', u'つぶやき投稿'), #自分向け
    ('MURMUR_TO_F', u'つぶやき投稿'), #読者向け
    ('MURMUR_REPLY', u'つぶやきのコメント(返信)'),
    ('MURMUR_SYMPATHY', u'つぶやきの共感'),

    ('COMMUNITY_JOIN', u'コミュニティ参加'), #自分向け
    ('COMMUNITY_JOIN_TO_F', u'コミュニティ参加'), #読者向け

    ('TWITTER_TO_F', u'Twitterのつぶやき'), #読者向け
    ('TWITTER_REPLY_TO_F', u'Twitterの返信'), #読者向け

    ('OFFICIAL_NEWS', u'編集部からの知らせ'), #ユーザ全員向け
)
NOTICE_TYPES_DICT = dict(NOTICE_TYPES)

# NOTICE_MEDIAを増やすと、MEDIA_DEFAULTSにも増やさないと通知が来ない
NOTICE_MEDIA = (
    ('EMAIL',  u'メール'),
    ('NEWS',  u'マイページの知らせ'), # 読者のタイムライン
    ('TIMELINE',  u'マイページのタイムライン'), # タイムライン
    ('REPLIES',  u'マイページのコメントリスト'),
    ('SYMPATHY',  u'マイページの共感リスト'),
)

# MEDIA_DEFALTSに入ってない場合、通知を送信しない。
MEDIA_DEFAULTS = {
    'SIGNUP': {
        'EMAIL': True,
    },
    'SIGNUP_COMPLETE': {
        'EMAIL': True,
    },
    'REMIND_PASSWD': {
        'EMAIL': True,
    },
    'INQUIRY': {
        'EMAIL': True,
    },
    'CHANGE_EMAIL': {
        'EMAIL': True,
    },
    'CHANGE_EMAIL_COMPLETE': {
        'EMAIL': True,
    },
    'ANSWER_TO_Q': {
        'EMAIL': True,     
        'NEWS': True,     
    },
    'SUPPL_ANSWER_TO_Q': {
        'EMAIL': True,  
    },
    'RATING_TO_A': {
        'EMAIL': True,
    },
    'BESTANSWER_TO_A': {
        'EMAIL': True,
    },
    'SUPPL_QUESTION_TO_A': {
        'EMAIL': True,
    },
    'REMOVE_QUESTION_TO_Q': {
        'EMAIL': True,
    },
    'RESIGN_COMPLETE': {
        'EMAIL': True,
    },
    'QUESTION': {
        'TIMELINE': True,
        'EMAIL': True,
    },
    'QUESTION_TO_F': {
        'TIMELINE': True,
    },
    'ANSWER_TO_A': {
        'TIMELINE': True,
        #'EMAIL': True,
    },
    'ANSWER_TO_F': {
        'TIMELINE': True,
    },
    'THANKS_TO_A': {
        'EMAIL': True,
        'NEWS': True,
    },
    'THANKSALL_TO_A': {
        'EMAIL': True,
    },
    'CLOSE_QUESTION_TO_Q': {
        'EMAIL': True,
    },
    'REVISE_MAILADDR': {
        'EMAIL': True,
    },
    'REVISED_MAILADDR': {
        'EMAIL': True,
    },
    'REMIND_RATING': {
        'EMAIL': True,
    },
    'INQUIRY': {
        'EMAIL': True,
    },
    'INQUIRY_STAFF': {
        'EMAIL': True,
    },
    'INQUIRY_POLICE': {
        'EMAIL': True,
    },
    'FOLLOW_SUBSCRIBER': {
        'EMAIL': True,
    },
    'EXCHANGE_AMEGOLD': {
        'EMAIL': True,
    },
    'EXCHANGE_LIFEMILE': {
        'EMAIL': True,
    },
    'DAILY_STAT_REPORT': {
        'EMAIL': True,
    },
    'BEST_ANS_WARNING_MAIL': {
        'EMAIL': True,
    },
    'DENY_QUESTION_USER': {
        'EMAIL': True,
    },
    'ALERT_QUESTIONAHOLIC': {
        'EMAIL': True,
    },
    'MURMUR_TO_SELF': {
        'TIMELINE': True,
    },
    'MURMUR_TO_F': {
        'TIMELINE': True,
    },
    'MURMUR_REPLY': {
        'NEWS': True,
        'REPLIES': True,
    },
    'MURMUR_SYMPATHY': {
        'NEWS': True,
        'SYMPATHY': True,
    },
    'COMMUNITY_JOIN': {
        'TIMELINE': True,
    },
    'COMMUNITY_JOIN_TO_F': {
        'TIMELINE': True,
    },
    'TWITTER_TO_F': {
        'TIMELINE': True,
    },
    'TWITTER_REPLY_TO_F': {
        'REPLIES': True,
    },
    'OFFICIAL_NEWS': {
        'NEWS':True,
    },
}
