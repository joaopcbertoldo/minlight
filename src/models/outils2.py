from numpy import sqrt


def verifier_cables(cables, maisonette, source, chambre, n_discretisation_cables, bilan_incomplet=False):

    bilan = {}
    message_standard = \
        {
            'maisonette' : 'ok',
            'source'     : 'ok',
            'chambre'    : 'ok',
            'croisement' : 'ok'
        }

    for cable in cables:
        bilan[cable.nom_sommet_source] = message_standard

    for cable in cables:

        # maisonette
        if cable.intersection_avec_pave(maisonette, n_discretisation_cables):
            bilan[cable.nom_sommet_source]['maisonette'] = '!'

            if bilan_incomplet:
                break

        # source
        if cable.intersection_avec_pave(source, n_discretisation_cables):
            bilan[cable.nom_sommet_source]['source'] = '!'

            if bilan_incomplet:
                break

        # chambre
        if not cable.entierement_dans_pave(chambre):
            bilan[cable.nom_sommet_source]['chambre'] = '!'

            if bilan_incomplet:
                break

        # croisements
        for autre_cable in cables:
            if autre_cable == cable:
                pass
            else:
                if cable.intersects_cable(autre_cable):
                    bilan[cable.nom_sommet_source]['croisement'] = '!'

                    if bilan_incomplet:
                        break

    return bilan


def bilan_cables_tout_ok(bilan_cables):
    resumes_cables = list(bilan_cables.values())
    return all(message == 'ok' for resume in resumes_cables for message in list(resume.values()))


def solutions_formule_quadratique(a, b, c):
    return ((-b - sqrt(b*b - 4*a*c))/(2*a),(-b + sqrt(b*b - 4*a*c))/(2*a))

def get_plane_normal(surface,verticies,reference_point):
    centre_plane = verticies[surface[0]] + verticies[surface[1]] + verticies[surface[2]] + verticies[surface[3]]
    centre_plane/=4
    normal = centre_plane - reference_point

    return normal.get_direction()
