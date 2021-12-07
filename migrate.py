# conda create --name myenv
# conda activate myenv
# conda install -c anaconda mysql-connector-python
from mysql2 import MySql

old_db = ['gaiascreen-db.czh3n6qtw0t1.ca-central-1.rds.amazonaws.com',
            'admin',
            '5jFMfF3LFDuK#%Uj',
            'gaiascreen']

new_db = ['workspacedb.czh3n6qtw0t1.ca-central-1.rds.amazonaws.com',
            'gaiadigits',
            'GaiaDigits2020#',
            'workspace']

def get_n_userid(ouser, users_new):
    founds = [nuser for nuser in users_new if nuser[1].lower() == ouser[1].lower()]
    if not founds:
        # print("no corresponding new user for old user", ouser)
        return 'no'
    return founds[0][0]

def insert_trackings(dh_o, dh_n, userid_map):
    ############################################################
    trackings_old = dh_o.query("""
    select * from Trackings where userID in (
        select Users.userID from Users
        join Accesses on Users.userID = Accesses.userID
        join Organizations on Organizations.orgID=Accesses.orgID where orgName='Windsor Essex Children’s Aid Society'
    )
    """)
    trackings_new = []
    for r in trackings_old:
        r_n = [*r, 'f1046008-fdd5-49af-a520-f1c709335c28', 'ce5e9d13-e668-4ab8-b87f-81269d8144ac']
        r_n[1] = userid_map[r[1]]
        trackings_new.append(r_n)
    print(len(trackings_new))
    # print(trackings_new[:10])

    for r in trackings_new[1:]:
        dh_n.execute_many("""INSERT INTO trackings(userID, triggered, createdAt, updatedAt, tenantId, locationId) 
                                VALUES(%s, %s, %s, %s, %s, %s)""",
                          [r[1:]])

def insert_records(dh_o, dh_n, userid_map, questionid_map, trackingid_map):
    records_old = dh_o.query("""
        select * from Records where userID in (
        select Users.userID from Users
        join Accesses on Users.userID = Accesses.userID
        join Organizations on Organizations.orgID=Accesses.orgID where orgName='Windsor Essex Children’s Aid Society'
        )
        """)
    records_new = []
    for r in records_old:
        r_n = [*r[1:]]
        r_n[0] = questionid_map[r[1]]
        r_n[1] = trackingid_map[r[2]]
        r_n[2] = userid_map[r[3]]
        records_new.append(r_n)
    print(len(records_new))
    print(records_new[:10])

    # [126, 289, 'e0120ae4-6c71-4570-9aaa-e4690f780e28', 'No', 0, datetime.datetime(2020, 11, 27, 17, 27, 10),
    #  datetime.datetime(2020, 11, 27, 17, 27, 10)]
    records_trial = records_new
    # print("records_trial", records_trial)
    print("=============")
    step = 100
    total = 0
    for i in range(0, len(records_trial), step):
        insertings = records_trial[i: min(i+step, len(records_trial))]
        total += len(insertings)
        print("insertings progress %d/%d" % (total, len(records_trial)))
        dh_n.execute_many("""INSERT INTO records(questionID, trackingID, userID, answer, triggered, createdAt, updatedAt)
                                    VALUES(%s, %s, %s, %s, %s, %s, %s)""",
                          insertings)

def main():
    dh_o = MySql(old_db[0], old_db[1], old_db[2], old_db[3])
    users_old = dh_o.query("""
        select Users.userID as id, Users.username as name from Users
        join Accesses on Users.userID = Accesses.userID
        join Organizations on Organizations.orgID=Accesses.orgID where orgName='Windsor Essex Children’s Aid Society'
        """
        )
    # dh_n = MySql(*new_db)

    dh_n = MySql(new_db[0], new_db[1], new_db[2], new_db[3])
    users_new = dh_n.query("select id, email from wsp_user where tenant_code='wecas'")

    userid_map = { ouser[0]: get_n_userid(ouser, users_new) for ouser in users_old }
    print(userid_map)

    #######################################################
    trackingids_old = dh_o.query("""
        select trackingID, createdAt from Trackings where userID in (
        select Users.userID from Users
        join Accesses on Users.userID = Accesses.userID
        join Organizations on Organizations.orgID=Accesses.orgID where orgName='Windsor Essex Children’s Aid Society'
        ) and userID != 115 order by createdAt desc""")
    trackingids_new = dh_n.query("""select trackingID, createdAt from trackings 
                                    where trackingID > 288 and updatedAt is not null
                                    order by createdAt desc""")
    trackings = zip(trackingids_old, trackingids_new)
    for o,n in trackings:
        assert(o[1] == n[1]), f"{o} != {n}"
    trackingids_map = { o[0]:n[0] for o, n in zip(trackingids_old, trackingids_new) }
    print("trackingids_map len", len(trackingids_map))

    questionsid_map = {
        87:126,
        88:129,
        89:128,
        94:130,
        95:135,
        96:132,
        97:137,
        109:133,
        110:134,
        111:138,
        114:139,
        126:127,
        129:131,
        371:136
    }

    insert_records(dh_o, dh_n, userid_map, questionsid_map, trackingids_map)

if __name__ == '__main__':
    main()