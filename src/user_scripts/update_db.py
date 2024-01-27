from service import UpdateDBService, FootballService

update_service = UpdateDBService(
    reference_club='Chelsea FC',
    traitors=['Kai Havertz', 'Mason Mount'],
)

update_service.update_all()

