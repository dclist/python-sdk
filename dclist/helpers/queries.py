class Queries:
    postBotStats = """mutation postBotStats($stats: BotStatsInput!) { postBotStats(stats: $stats) }"""
    getBotById = """query getBotById($botId: String!) { getBot(botId: $botId) { $FIELDS$ } }"""
    getUser = """query getUser($userId: String!) { getUser(userId: $userId) { $FIELDS$ } }"""
    getUserComment = """query getUserComment($userId: String!) { getUserComment(userId: $userId) { $FIELDS$ } }"""
    isUserVoted = """query isUserVoted($userId: String!) { isUserVoted(userId: $userId) }"""
    # if you guys wanna implement wss:subscribe we're always open to prs and contributions!

    @staticmethod
    def fields(query:str, fields) -> str:
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