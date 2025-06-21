### 🛠️ Admin APIs

| Action                            | Method | Endpoint                           |
| --------------------------------- | ------ | ---------------------------------- |
| View All Analytics                | GET    | `/api/analytics/`                  |
| View Analytics for Specific Event | GET    | `/api/analytics/?event={event_id}` |
| View Audit Logs                   | GET    | `/api/auditlogs/`                  |

### 🔐 Authentication APIs

| Action             | Method | Endpoint                                           |
| ------------------ | ------ | -------------------------------------------------- |
| Admin Registration | POST   | `/user/admin/register/`                            |
| Admin Login        | POST   | `/user/admin/login/`                               |
| Admin Resend OTP   | POST   | `/user/resend-otp/resend-verification/`            |
| OTP Verification   | POST   | `/user/verify-otp/`                                |
| User Registration  | POST   | `/user/auth/users/`                                |
| User Login         | POST   | `/auth/token/login/`                               |
| User Resend OTP    | POST   | `/user/resend-otp/resend-verification/?admin=true` |
| OTP Verification   | POST   | `/user/verify-otp/`                                |

> 📒 **Note:** OTP Verification
> Same for both Admin and User and after resending OTP same endpoint can be used for
> OTP verification

### ✳️For OTP and other Utilities

For detailed documentation on OTP and other utilities, see the [`/docs/utilities/UTILITIES.md`](/docs/utilities/UTILITIES.md) file.  
Or explore the source code in the [`/user/utils/`](/user/utils/) directory.

### 🧑‍💼 Organizer APIs

| Action            | Method | Endpoint                        |
| ----------------- | ------ | ------------------------------- |
| Create Organizer  | POST   | `/api/organizers/`              |
| List Organizers   | GET    | `/api/organizers/`              |
| Approve Organizer | POST   | `/api/organizers/{id}/approve/` |
| Reject Organizer  | POST   | `/api/organizers/{id}/reject/`  |

### 🎉 Event APIs

| Action              | Method | Endpoint                          |
| ------------------- | ------ | --------------------------------- |
| Create Event        | POST   | `/api/events/`                    |
| List Events         | GET    | `/api/events/`                    |
| Update Event        | PATCH  | `/api/events/{id}/`               |
| Get Event by ID     | GET    | `/api/events/{id}/`               |
| Approve Event       | POST   | `/api/events/{id}/approve/`       |
| Reject Event        | POST   | `/api/events/{id}/reject/`        |
| Change Event Status | POST   | `/api/events/{id}/change_status/` |

### 🎟️ Ticket APIs

| Action        | Method | Endpoint        |
| ------------- | ------ | --------------- |
| Create Ticket | POST   | `/api/tickets/` |
| List Tickets  | GET    | `/api/tickets/` |

### 📝 Booking APIs

| Action               | Method | Endpoint                             |
| -------------------- | ------ | ------------------------------------ |
| Create Booking       | POST   | `/api/bookings/`                     |
| List Bookings        | GET    | `/api/bookings/`                     |
| Booking with Payment | POST   | `/api/bookings/create_with_payment/` |

### 🖼️ Media APIs

| Action             | Method | Endpoint                        |
| ------------------ | ------ | ------------------------------- |
| Upload Media       | POST   | `/api/media/`                   |
| List Media         | GET    | `/api/media/`                   |
| Get Media by ID    | GET    | `/api/media/{id}/`              |
| Get Media by Event | GET    | `/api/events/{event_id}/media/` |

### 🔔 Notification APIs

| Action              | Method | Endpoint              |
| ------------------- | ------ | --------------------- |
| Create Notification | POST   | `/api/notifications/` |
| List Notifications  | GET    | `/api/notifications/` |

### ⭐ Review APIs

| Action                | Method | Endpoint                         |
| --------------------- | ------ | -------------------------------- |
| Create Review         | POST   | `/api/reviews/`                  |
| List Reviews          | GET    | `/api/reviews/`                  |
| Get Reviews for Event | GET    | `/api/reviews/?event={event_id}` |

### 📊 Analytics APIs

| Action                | Method | Endpoint                          |
| --------------------- | ------ | --------------------------------- |
| Create Analytics      | POST   | `/api/analytics/`                 |
| List Analytics        | GET    | `/api/analytics/`                 |
| Increment Event View  | POST   | `/api/analytics/increment-view/`  |
| Increment Event Click | POST   | `/api/analytics/increment-click/` |

### Summary Table

| Action        | Endpoint                          | Who Can Do It | Effect                        |
| ------------- | --------------------------------- | ------------- | ----------------------------- |
| is_approve    | `/user/staff-approval/approve/`   | Super Admin   | is_staff status → approved    |
| Approve Org   | `/api/organizers/{id}/approve/`   | Admin         | Organizer status → approved   |
| Reject Org    | `/api/organizers/{id}/reject/`    | Admin         | Organizer status → rejected   |
| Approve Event | `/api/events/{id}/approve/`       | Admin         | Event status → published      |
| Reject Event  | `/api/events/{id}/reject/`        | Admin         | Event status → cancelled      |
| Change Status | `/api/events/{id}/change_status/` | Admin         | Set event status (valid only) |

> 📒 **Note:** Check bash bellow for JSON request for is_staff approval (!! superuser action !!)

```bash
{
  "user_id": {id}
}
```
