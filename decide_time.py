def decide(conb, cou_a, sam):
    import numpy as np
    a = 0
    b = 0
    c = 0
    d = 0
    z = 0
    e = 100
    f = 100
    lis = []
    n = conb.shape[0]
    conb = np.tril(conb)
    conb[np.eye(n, dtype=bool)] = 0

    # 探索
    for x in conb:
        for y in x:
            c = a
            d = b
            while conb[c, d] >= 0.6:
                e = 0
                # print(conb[c,d])
                c = 1+c
                d = 1+d
                z = 1+z
                if z >= 1000:
                    z = 0
                    # print(c-z,'行',d-z,'列')
                    if (c-z)-(d-z) > 750:
                        lis.append(4*(c-z))
                        lis.append(4*(d-z))
                    a = c
                    b = d
                    break
                if c > conb.shape[0]-1 or d > conb.shape[0]-1:
                    f = 0
                    break
            if e == 0:
                b = d
                a = c
                e = 100
            else:
                b = b+1
                if b > conb.shape[0]-1:
                    break
            if f == 0:
                break

        a = a+1
        b = 0
        if a > conb.shape[0]-1:
            break

    if not lis:  # 類似度の候補時間がなければパワースペクトラムの最大値の時間を使用する
        print(lis, "power")
        return cou_a

    wh = 3000  # 似ているところ前後範囲指定今は30秒
    haniM = []  # 各座標の最大値
    max_1 = -9999999
    for z in lis:
        for i in range(z-wh, z+wh):
            if sam[i] > max_1:
                max_1 = sam[i]
        haniM.append(max_1)
        max_1 = -9999999

    cou_a = 0

    for i in haniM:
        print(sam.index(i))
    return sam.index(max(haniM))
