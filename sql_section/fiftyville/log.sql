-- Keep a log of any SQL queries you execute as you solve the mystery.

-- First of all, i want more information about the crime scene reports, so i query the crime_scene_reports table matching the year, month, day, street
SELECT * FROM crime_scene_reports WHERE day = 28 AND month = 7 AND year = 2023 AND street = 'Humphrey Street';

-- Now we know there are 3 witness's that mention a bakery. Now i want to know more info based on the interviews transcripts
SELECT * FROM interviews WHERE transcript LIKE "%bakery%" AND day = 28 AND month = 7 AND year = 2023

-- Starting from the first witnesse's transcript let's check the bakery_security_logs. The transcript mention ten minutes of the theft and we know the theft was at 10:15
SELECT * FROM bakery_security_logs WHERE day = 28 AND month = 7 AND year = 2023 AND hour = 10 AND minute BETWEEN 15 AND 25;

-- Now we have a license_plate of 8 cars. Let's check rthe second witness's transcription and search for ATM logs
SELECT * FROM atm_transactions WHERE day = 28 AND month = 7 AND year = 2023 AND atm_location = "Leggett Street" AND transaction_type = "withdraw";

-- Now we know 8 different withdrawind account numbers. Let's check the last witness's transcript and search for a phone log and a flyght ticket
SELECT * FROM phone_calls WHERE day = 28 AND month = 7 AND year = 2023 AND duration < 60;
SELECT * FROM flights WHERE day = 29 AND month = 7 AND year = 2023 ORDER BY hour, minute ASC LIMIT 1;

-- Now we have all the information we needs, lo let's make the query to know the thief. Starting from people table. The thief is Bruce
SELECT name FROM people WHERE people.license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE day = 28 AND month = 7 AND year = 2023 AND hour = 10 AND minute BETWEEN 15 AND 25) AND people.id IN (SELECT person_id FROM bank_accounts JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number WHERE atm_transactions.day = 28 AND atm_transactions.month = 7 AND atm_transactions.year = 2023 AND transaction_type = "withdraw" AND atm_transactions.atm_location = "Leggett Street") AND people.phone_number IN (SELECT caller FROM phone_calls WHERE day = 28 AND month = 7 AND year = 2023 AND duration < 60) AND people.passport_number IN (SELECT passport_number FROM passengers WHERE flight_id IN (SELECT id FROM flights WHERE day = 29 AND month = 7 AND year = 2023 ORDER BY hour, minute ASC LIMIT 1));

-- To know in what city the thief escaped to by using destination_airport_id retrieved previously in the 6th query. The result is New York City.
SELECT city FROM airports WHERE id = 4;

-- Finally, let's catch the accomplice's name. To do this, let's check the phone calls by adding the thief name. The accomplice is Robin
SELECT name FROM people WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE day = 28 AND month = 7 AND year = 2023 AND caller = (select phone_number FROM people WHERE name = "Bruce") AND duration < 60);