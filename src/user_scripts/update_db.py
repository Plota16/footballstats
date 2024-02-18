from src.service import UpdateDBService, FootballService

update_service = UpdateDBService(
    reference_club='Chelsea FC',
    traitors=['Kai Havertz', 'Mason Mount','Callum Hudson-Odoi'],
)

update_service.update_all()

