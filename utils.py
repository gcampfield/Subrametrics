# def rnd(n):
#     '''round a number to the thousands place'''
#     place = 0.001
#     if n % place < place * 5: return n - (n % place)
#     return n + place - (n % place)

def darken((r, g, b), p):
    '''darkens the rgb color c by p percent'''
    # return (rnd(r * (1 - p)), rnd(g * (1 - p)), rnd(b * (1 - p)))
    return (r * (1 - p), g * (1 - p), b * (1 - p))
