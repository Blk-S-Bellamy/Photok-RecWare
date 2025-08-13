# template of data return
retdata = {"failed" : False,
           "data" : None,
           'errors' : []
           }


# fails and appends errors before returning dict
def failme(errors : (list, str)):
    global retdata
    ret = retdata
    print(errors)

    ret['failed'] = True
    if type(errors) == str:
        ret['errors'].append(errors)
    elif type(errors) == list:
        ret['errors'].extend(errors)
    else:
        pass
    return ret
