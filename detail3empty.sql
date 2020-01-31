USE shogi;
select iteration, tournament_name, detail1, detail2, detail3 from matches
where detail1 LIKE '%リーグ%' and detail3 = ""
group by iteration, tournament_name
order by tournament_name, iteration;