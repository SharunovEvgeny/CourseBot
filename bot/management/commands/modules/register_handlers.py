from bot.management.commands.dialogs.general.states import General


def register_handlers(dp, handlers):
    states = General.all_states

    for h, i in enumerate(handlers):
        dp.register_message_handler(h, state=states[i])
        if i > 0:
            dp.register_callback_query_handler(h, text="back", state=states[i - 1])
