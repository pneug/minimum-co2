# qm ist halbe Dachfläche:
def kosten_normal(qm, jahre):
    k_nach_qm = (4500 * qm / 30) * 0.27
    return int(k_nach_qm * sum([1.02 ** x for x in range(jahre)]))


def kosten_anschaffung(qm):
    return 1000 + 275 * qm


def kosten_mit(qm, jahre):
    anschaffung = kosten_anschaffung(qm)
    return int(anschaffung + sum([(4500 * qm / 30 * 1.02 ** x - 100 * qm * 0.99 ** x) * 0.27 for x in range(jahre)]))


if __name__ == '__main__':
    qm = 30
    print(f"Jahr: <Normal:  | Solar: ")
    for i in range(1, 25):
        print(f"{i}| {kosten_normal(qm, i)} | {kosten_mit(qm, i)}")