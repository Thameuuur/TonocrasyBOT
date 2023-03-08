import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create a bot instance
bot = Bot(token='6168225890:AAHnR2aqjUaFCIwG1mYA-TQ_Inpqw0PzJrw')

# Create a Dispatcher instance
dp = Dispatcher(bot, storage=MemoryStorage())

# Define the States
class Form(StatesGroup):
    name = State()          # ask for user's name
    dao_name = State()      # ask for user's dao name
    dao_purpose = State()   # ask for the purpose of the dao
    is_council = State()    # ask if the user is the only council for the moment
    allow_proposals = State()   # ask if the user will allow community to add proposals
    allow_voting = State()  # ask if the user will allow community to vote on proposals
    confirm_data = State()  # ask the user to confirm their input

# Define the start command handler
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Hi there! I'm Jaaf, the DAO creator bot. Let's get started by getting to know you first. What's your name?")
    await Form.name.set()

# Define the name handler
@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply(f"Nice to meet you, {data['name']}! What is the name of your DAO?")
    await Form.dao_name.set()

# Define the dao_name handler
@dp.message_handler(state=Form.dao_name)
async def process_dao_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['dao_name'] = message.text

    await message.reply(f"{data['dao_name']} sounds like a great name for a DAO! What is the purpose of your DAO?")
    await Form.dao_purpose.set()

# Define the dao_purpose handler
@dp.message_handler(state=Form.dao_purpose)
async def process_dao_purpose(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['dao_purpose'] = message.text

    await message.reply(f"{data['dao_purpose']} is a noble purpose indeed! Will you be the only council for the moment? Please answer Yes or No.")
    await Form.is_council.set()

# Define the is_council handler
@dp.message_handler(state=Form.is_council)
async def process_is_council(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['is_council'] = message.text.lower() in ['yes', 'y']

    await message.reply("Got it! Will you allow the community to add any kind of proposals? Please answer Yes or No.")
    await Form.allow_proposals.set()

# Define the allow_proposals handler
@dp.message_handler(state=Form.allow_proposals)
async def process_allow_proposals(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['allow_proposals'] = message.text.lower() in ['yes', 'y']

        await message.reply("Thanks! Will you allow the community to vote on proposals? Please answer Yes or No.")
        await Form.allow_voting.set()

# Define the allow_voting handler
@dp.message_handler(state=Form.allow_voting)
async def process_allow_voting(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['allow_voting'] = message.text.lower() in ['yes', 'y']

    # Ask the user to confirm their input
    reply = f"Thanks for providing your information. Here's what I got:\n\nName: {data['name']}\nDAO Name: {data['dao_name']}\nPurpose: {data['dao_purpose']}\nOnly Council: {'Yes' if data['is_council'] else 'No'}\nAllow Proposals: {'Yes' if data['allow_proposals'] else 'No'}\nAllow Voting: {'Yes' if data['allow_voting'] else 'No'}\n\nIs this correct? Please answer Yes or No."
    await message.reply(reply, parse_mode=ParseMode.MARKDOWN)
    await Form.confirm_data.set()

# Define the confirm_data handler
@dp.message_handler(state=Form.confirm_data)
async def process_confirm_data(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        confirm = message.text.lower() in ['yes', 'y']
        if confirm:
            # TODO: Save the data to a database or send it somewhere
            await message.reply("Great! Your DAO has been created.")
        else:
            await message.reply("Sorry about that. Let's start over.")
        # Reset the state machine
        await state.finish()

# Define the error handler
@dp.errors_handler()
async def errors_handler(update, error):
    logging.error(f"Update {update} caused error {error}")

# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
