from api import TransfermarktAPI
from service import UpdateDBService, FootballService

update_service = UpdateDBService(
    reference_club='Chelsea FC',
    traitors=['Kai Havertz', 'Mason Mount'],
)

update_service.update_all()

f_service = FootballService()
df = f_service.get_data_agg()
bio_df = f_service.get_bio()
#
# tmp = df.join(bio_df.set_index('playerID'), on='playerID', lsuffix='p')
# tmp = tmp [['playerID', 'name', 'minutesPlayed', 'goals', 'assists', 'GA', 'goals_p90', 'assists_p90', 'GA_p90']]
# tmp.sort_values(by='GA_p90', inplace=True, reversed=True)
# pass