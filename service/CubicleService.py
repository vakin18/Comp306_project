import repository.CubicleRepository as CR

def createCubicle(cubicle_number: str, location: str):
    cubicle_exists = CR.cubicleExists(cubicle_number)

    error_message = ""
    if cubicle_exists:
        
        error_message = "This cubicle already exists. Cannot create."
        return error_message
    
    CR.createCubicle(cubicle_number, location)

def getAllCubicles():
    cubicle_tuples = CR.getAllCubicles()
    cubicle_list = [cubicle[0] for cubicle in cubicle_tuples]
    return cubicle_list

def cubicleExists(cubicle_number: str):
    return CR.cubicleExists(cubicle_number)

