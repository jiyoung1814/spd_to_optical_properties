import colour
from flask import Flask, jsonify, request

app = Flask(__name__)
portNum = 8080

@app.route('/spd/getAll', methods=['POST'])
def getAll():
    spd = request.json['spd']
    # res = jsonify({})
    data = {}
    # try:
    sd = colour.SpectralDistribution(spd)

    data['XYZ'] = getXYZ(sd)
    data['xyz'] = getxyz(sd)

    data['CCT'] = getCCT(sd)
    data['lux'] = getLux(sd)

    data['CRI'] = getCRI(sd)
    data['CQS'] = getCQS(sd)


    res = jsonify(data)
    res.status_code = 200
    # except:
    #     res.status_code = 400

    return res


def getXYZ(sd):
    cmfs = colour.MSDS_CMFS['CIE 1931 2 Degree Standard Observer']
    illuminant = colour.SDS_ILLUMINANTS['D65']
    XYZ = colour.sd_to_XYZ(sd)
    return [Tristimulus * 729 for Tristimulus in XYZ.tolist()]


def getxyz(sd):
    XYZ = getXYZ(sd)
    xy = colour.XYZ_to_xy(XYZ)
    xyz = [xy[0], xy[1], (1 - xy[0] - xy[1])]
    # xyz = {
    #     'x': xy[0],
    #     'y': xy[1],
    #     'z': 1 - xy[0] - xy[1]
    # }
    return xyz


def getCCT(sd):
    xyz = getxyz(sd)
    cct = colour.xy_to_CCT(xyz[0:2], "McCamy 1992")
    return cct


def getLux(sd):
    XYZ = getXYZ(sd)
    lux = XYZ[1]
    return lux


def getCRI(sd):
    cri_all = colour.colour_rendering_index(sd, additional_data=True)
    cri = {
        "ra": cri_all.Q_a,
        "r1": cri_all.Q_as[1].Q_a,
        "r2": cri_all.Q_as[2].Q_a,
        "r3": cri_all.Q_as[3].Q_a,
        "r4": cri_all.Q_as[4].Q_a,
        "r5": cri_all.Q_as[5].Q_a,
        "r6": cri_all.Q_as[6].Q_a,
        "r7": cri_all.Q_as[7].Q_a,
        "r8": cri_all.Q_as[8].Q_a,
        "r9": cri_all.Q_as[9].Q_a,
        "r10": cri_all.Q_as[10].Q_a,
        "r11": cri_all.Q_as[11].Q_a,
        "r12": cri_all.Q_as[12].Q_a,
        "r13": cri_all.Q_as[13].Q_a,
        "r14": cri_all.Q_as[14].Q_a,
    }
    return cri


def getCQS(sd):
    cqs_all = colour.colour_quality_scale(sd, additional_data=True)
    cqs = {
        "ra": cqs_all.Q_a,
        "vs1": cqs_all.Q_as[1].Q_a,
        "vs2": cqs_all.Q_as[2].Q_a,
        "vs3": cqs_all.Q_as[3].Q_a,
        "vs4": cqs_all.Q_as[4].Q_a,
        "vs5": cqs_all.Q_as[5].Q_a,
        "vs6": cqs_all.Q_as[6].Q_a,
        "vs7": cqs_all.Q_as[7].Q_a,
        "vs8": cqs_all.Q_as[8].Q_a,
        "vs9": cqs_all.Q_as[9].Q_a,
        "vs10": cqs_all.Q_as[10].Q_a,
        "vs11": cqs_all.Q_as[11].Q_a,
        "vs12": cqs_all.Q_as[12].Q_a,
        "vs13": cqs_all.Q_as[13].Q_a,
        "vs14": cqs_all.Q_as[14].Q_a,
        "vs15": cqs_all.Q_as[15].Q_a
    }
    return cqs


if __name__ == '__main__':
    app.run(port=portNum)
