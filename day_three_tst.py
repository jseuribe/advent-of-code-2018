import re

claims_fname = "claims_tst.txt"

fab_arr = [[0 for i in range(1000)] for j in range(1000)]
fab_check_arr = [[False for i in range(1000)] for j in range(1000)]

def get_claims():
    claims_list = []
    raw_claims = []

    with open(claims_fname, 'r') as claims_f:
        raw_claims = [ln.rstrip() for ln in claims_f.readlines()]

    for raw_claim in raw_claims:
        c_claim = {}

        #Get the claim ID first
        c_claim_id = re.sub('#', '', raw_claim.split('@')[0])
        #Get the coordinates
        c_claim_coords = (int(raw_claim.split('@')[1].split(':')[0].split(',')[0].strip()), int(raw_claim.split('@')[1].split(':')[0].split(',')[1].strip()))

        #Get the dimensions
        c_claim_area = (int(raw_claim.split('@')[1].split(':')[1].split('x')[0].strip()), int(raw_claim.split('@')[1].split(':')[1].split('x')[1].strip()))
        print(c_claim_id)
        print(c_claim_coords)
        print(c_claim_area)

        c_claim['id'] = c_claim_id
        c_claim['coords'] = c_claim_coords
        c_claim['area'] = c_claim_area

        claims_list.append(c_claim)
    
    return claims_list


def incre_maps(count_map, bool_map, claim):
    y_start = claim['coords'][0]
    x_start = claim['coords'][1]
    x_end = x_start + claim['area'][1]
    y_end = y_start + claim['area'][0]

    print("PROCESSING CLAIM:", claim['id'])
    print(x_start, y_start)
    for i in range(x_start, x_end):
        for j in range(y_start, y_end):
            print("PROCESSING INDEX:", i, j)
            count_map[i][j] += 1

    return count_map


if __name__ == "__main__":

    claims_list = get_claims()

    for claim in claims_list:
        fab_arr = incre_maps(fab_arr, fab_check_arr, claim)

    overlapping = 0
    for row in fab_arr:
        print(row)
        for elem in row:
            if elem > 1:
                overlapping += 1

    print("OVERLAPPING INCHES:", overlapping)

