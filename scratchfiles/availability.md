Available Range
- availrange ID
- start_date
- end_date
- space ID (foreign key)

Bookings
- Booking ID
- start_date
- end_date
- user ID (foreign key)
- space ID (foreign key)


Host selects an available range -> start of range & end of range

Is userbooking.startofrange > available.startofrange?
Is userbooking.endofrange < available.endofrange?

for booking in bookings:
    Is userbooking.startofrange > booking.startofrange?
    Is userbooking.startofrange > booking.endofrange?


Display:

SELECT FROM availrange * WHERE space_id = 1
[{start:date,end:date},range2]
for range in availranges:
    cleverdatetimestuff
availdays =[day,day,day]
SELECT FROM bookings * WHERE space_id = 1
[range1,range2]