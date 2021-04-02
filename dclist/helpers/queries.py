class Queries:
    postBotStats = """mutation postBotStats($stats: BotStatsInput!) { postBotStats(stats: $stats) }"""
    getBotById = """query getBotById($botId: String!) { getBot(botId: $botId) { $FIELDS$ } }"""
    getUser = """query getUser($userId: String!) { getUser(userId: $userId) { $FIELDS$ } }"""
    getUserComment = """query getUserComment($userId: String!) { getUserComment(userId: $userId) { $FIELDS$ } }"""
    isUserVoted = """query isUserVoted($userId: String!) { isUserVoted(userId: $userId) }"""
    SDKUpdateSubcription = """subscription SDKUpdateSubcription($topics: [SDKUpdateTypeEnum!]!) { sdkUpdates(topics: $topics) { type payload { ... on NewVoteSDKUpdatePayload { user { $FIELDS:VOTE:USER$ } } ... on NewCommentSDKUpdatePayload { comment { $FIELDS:VOTE:COMMENT$ } } } } }"""

    @staticmethod
    def fields(query:str, fields) -> str:
        query = query.replace('$FIELDS:VOTE:USER$', Queries.user_fields())
        query = query.replace('$FIELDS:VOTE:COMMENT$', Queries.comment_fields())
        return query.replace('$FIELDS$', str(fields))

    @staticmethod
    def user_fields() -> str:
        return """
        id
        username
        discriminator
        avatar
        website
        github
        """

    @staticmethod
    def bot_fields() -> str:
        return Queries.user_fields() + """
        stats {
            userCount
            guildCount
            voteCount
        }
        prefix
        prefixType
        tags
        """


    @staticmethod
    def comment_fields() -> str:
        return """
        type
        like
        content
        subject {  
            """ + Queries.user_fields() + """
        }
        author {  
            """ + Queries.user_fields() + """
        }
        """