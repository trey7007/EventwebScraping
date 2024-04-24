SELECT 
    e.city as "City",
    e.genre as "Genre",
    e.name as "Band",
    e.location as "Venue",
    case 
        strftime('%m', e.date) when '01' then 'January' when '02' then 'Febuary' when '03' then 'March' when '04' then 'April' when '05' then 'May' when '06' then 'June' when '07' then 'July' when '08' then 'August' when '09' then 'September' when '10' then 'October' when '11' then 'November' when '12' then 'December' 
        else '' end || ' ' ||
        strftime('%d', e.date) as "Date"    
FROM events e
WHERE e.date <= date('now', '+7 days') AND
    e.genre IS NOT "Country"
ORDER BY e.date;