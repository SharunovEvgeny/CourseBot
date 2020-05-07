from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery

from bot.management.commands.modules.custom_state import CustomState


class Button(BoundFilter):
    def __init__(self, key, contains=False):
        self.key = key
        self.contains = contains

    async def check(self, message) -> bool:
        if isinstance(message, Message):
            if self.contains:
                return self.key in message.text
            else:
                return message.text == self.key
        elif isinstance(message, CallbackQuery):
            if self.contains:
                return self.key in message.data
            else:
                return self.key == message.data


class CustomStateFilter(BoundFilter):
    key = 'custom_state'

    def __init__(self, dispatcher, custom_state: CustomState):
        self.custom_state = custom_state
        self.dispatcher = dispatcher

    async def check(self, message: types.Message) -> typing.Optional[typing.Dict[str, typing.Any]]:
        # print("Состояние: ", self.custom_state.state if not isinstance(self.custom_state, str) else self.custom_state)
        current_state = await self.dispatcher.current_state().get_state()
        if '*' == self.custom_state:
            for custom_sate in list(CustomState.get_instances()):
                print(custom_sate.state, current_state, custom_sate.state == current_state)
                if current_state in custom_sate.state:
                    return {'custom_state': custom_sate}
            raise Exception("ERROR: No custom_states with current state, make it or fuck it.")
        elif isinstance(self.custom_state, list):
            for state in self.custom_state:
                if state.state == current_state:
                    return {"custom_state": state}
        elif current_state == self.custom_state.state:
            return {"custom_state": self.custom_state}
        return None
