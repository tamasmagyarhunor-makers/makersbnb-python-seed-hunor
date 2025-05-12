# Makersbnb Design Doc

## Specifications

Any signed-up user can list a new space.
Users can list multiple spaces.
Users should be able to name their space, provide a short description of the space, and a price per night.
Users should be able to offer a range of dates where their space is available.
Any signed-up user can request to hire any space for one night, and this should be approved by the user that owns that space.
Nights for which a space has already been booked should not be available for users to book that space.
Until a user has confirmed a booking request, that space can still be booked for that night.

## Design Thoughts

### Requirements

Users can sign up an account*
Users can sign into an existing account*
Hosts can add new spaces*
Spaces have a name, description, and price per night
Spaces have a range of dates they are available
Hosts can set and change availability for their Spaces*
Users can see (available*) spaces for a date
Users can make a provisional booking for a space*
Users can confirm a provisional booking for their own spaces*
Users cannot book dates which are already booked and confirmed*

Additional assumptions I made:

Users might want to have their available range be extremely large/extend forever
Users might want multiple available ranges for their space availability
Users might want to book more than one night in a row

### Stored Information and Methods

User
- Username
- User ID
- Password
- Email address

User Repository
- Create user (inc password)*
- Check inputed password matches*
- change password*
- delete user*

Space
- Space ID
- Name
- Description
- Price per night
- Owner ID

Space Repository
- Create Space*
- List Spaces (opt: by owner)
- Edit Space*
- Delete Space*
- List available days*

AvailableRange*
- AvailRange ID
- Start_of_range
- end_of_range
- space ID
- Is date/date range within available range?*

AvailableRange Repository
- create availrange(spaceID, start, end)*
- delete available range*


Booking*
- Booking ID
- start of range
- end of range
- user ID
- space ID
- is date/date range booked?

Booking Repository*
- create booking
- delete booking
- update booking (extension?)
- list bookings by user ID
- list bookings by space ID




### DB Tables

Users
- User ID
- Username
- Password
- Email

Spaces
- Space ID
- Name
- Description
- Price per night
- User ID (foreign key)

Available Range
- availrange ID
- start of range
- end of range
- space ID (foreign key)

Bookings
- Booking ID
- start of range
- end of range
- user ID (foreign key)
- space ID (foreign key)




