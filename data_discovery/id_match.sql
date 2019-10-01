/*Scene_ID format LC8PPPRRRYYYYDDDLGN0[0,1]
 WHERE P = WRS_Path
       R = WRS_Row
       YYYY = year
       DDD = Day num out of 365
       LGN0 = "LGNO"
       [0,1] = either "0" or "1"*/
SELECT COUNT(*) FROM metadata WHERE substr(sceneID, 1, length(sceneID) - 1)
in (SELECT substr(ID, 1, length(ID) - 1) FROM scene_ids);
