# Dewey Decimal Discord Bot Project

## Objective
This project aims to create a simple tool for logging, viewing, and managing book references in the Dewey Decimal System form. The bot will be suitable for personal use and showcasing in a software engineering portfolio.

## Project Scope
The Dewey Decimal Discord Bot will provide the following key functionalities:

1. **Adding Book References:**
   - The bot will parse user input in the format: `B. <dewey_decimal> - <category> - <title>`.
   - It will automatically extract and store the Dewey Decimal number, category, and title in an Azure SQL database.

2. **Searching for Books:**
   - Users can search for books within a specified Dewey Decimal range using a command.
   - The bot will return a list of books that match the specified range, displaying their titles, Dewey Decimal numbers, and categories.

3. **Listing All Books:**
   - The bot will list all books stored in the database, ordered by Dewey Decimal numbers.
   - This feature helps users quickly view the entire library.

4. **Database Management:**
   - The project will use an Azure SQL database to store book references.
   - The database schema will include fields for `id`, `title`, `dewey_decimal`, and `category`.

5. **Error Handling and Logging:**
   - The bot will implement robust error handling to manage invalid inputs, database connection issues, and command errors.
   - A logging system will be set up to track bot activities and errors for easy debugging.

6. **Deployment and Demonstration:**
   - The bot will be deployed on a cloud platform (e.g., Azure App Service) for continuous availability.
   - This project will be used as part of a software engineering portfolio, showcasing skills in:
     - Backend development (Python, SQL)
     - Cloud integration (Azure SQL)
     - Bot development (Discord API)
     - Error handling and logging
     - Database design and management

## Technologies Used
- **Backend:** Python (`discord.py`)
- **Database:** Azure SQL Database
- **Deployment:** Azure App Service
- **Version Control:** GitHub for project management and collaboration

## Future Enhancements (Optional)
- **Exporting Library Data:** Allow users to export the library data to a CSV file.
- **Advanced Search:** Implement additional search filters (e.g., by category or title).
- **User Authentication:** Add user-specific libraries using Discord IDs.
- **Web Interface:** Develop a simple web interface for non-Discord users to view and manage the library.