from langchain.tools import tool
from typing import Optional
from datetime import datetime
from database.models import Employee, Ticket, Report, SessionLocal

@tool
def create_ticket(title: str, description: str, priority: str = "medium", assigned_to: Optional[str] = None) -> str:
    """Create a new support ticket in the system.
    
    Args:
        title: Brief title of the ticket
        description: Detailed description of the issue or request
        priority: Priority level (low, medium, high). Default is medium
        assigned_to: Name of person to assign the ticket to (optional)
    
    Returns:
        Confirmation message with ticket ID
    """
    db = SessionLocal()
    try:
        ticket = Ticket(
            title=title,
            description=description,
            priority=priority.lower(),
            assigned_to=assigned_to,
            status="open"
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return f"Ticket created successfully! Ticket ID: {ticket.id}, Title: '{title}', Priority: {priority}, Status: open"
    except Exception as e:
        db.rollback()
        return f"Error creating ticket: {str(e)}"
    finally:
        db.close()

@tool
def get_employee_info(identifier: str) -> str:
    """Fetch employee information by name or email.
    
    Args:
        identifier: Employee name or email address
    
    Returns:
        Employee details including name, position, department, and salary
    """
    db = SessionLocal()
    try:
        employee = db.query(Employee).filter(
            (Employee.name.ilike(f"%{identifier}%")) | 
            (Employee.email.ilike(f"%{identifier}%"))
        ).first()
        
        if employee:
            return (f"Employee: {employee.name}\n"
                   f"Email: {employee.email}\n"
                   f"Department: {employee.department}\n"
                   f"Position: {employee.position}\n"
                   f"Salary: ${employee.salary:,.2f}\n"
                   f"Hire Date: {employee.hire_date.strftime('%Y-%m-%d')}")
        else:
            return f"No employee found with identifier: {identifier}"
    except Exception as e:
        return f"Error fetching employee info: {str(e)}"
    finally:
        db.close()

@tool
def list_employees(department: Optional[str] = None) -> str:
    """List all employees or filter by department.
    
    Args:
        department: Optional department filter (e.g., Engineering, HR, Sales)
    
    Returns:
        List of employees with basic information
    """
    db = SessionLocal()
    try:
        query = db.query(Employee)
        if department:
            query = query.filter(Employee.department.ilike(f"%{department}%"))
        
        employees = query.all()
        
        if not employees:
            return f"No employees found{f' in {department} department' if department else ''}"
        
        result = f"Found {len(employees)} employee(s):\n\n"
        for emp in employees:
            result += f"- {emp.name} ({emp.position}, {emp.department})\n"
        
        return result
    except Exception as e:
        return f"Error listing employees: {str(e)}"
    finally:
        db.close()

@tool
def get_ticket_status(ticket_id: Optional[int] = None) -> str:
    """Get status of a specific ticket or list all open tickets.
    
    Args:
        ticket_id: Optional ticket ID to get specific ticket status
    
    Returns:
        Ticket status information
    """
    db = SessionLocal()
    try:
        if ticket_id:
            ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
            if ticket:
                return (f"Ticket #{ticket.id}: {ticket.title}\n"
                       f"Status: {ticket.status}\n"
                       f"Priority: {ticket.priority}\n"
                       f"Assigned to: {ticket.assigned_to or 'Unassigned'}\n"
                       f"Description: {ticket.description}\n"
                       f"Created: {ticket.created_at.strftime('%Y-%m-%d %H:%M')}")
            else:
                return f"Ticket #{ticket_id} not found"
        else:
            tickets = db.query(Ticket).filter(Ticket.status == "open").all()
            if not tickets:
                return "No open tickets found"
            
            result = f"Open Tickets ({len(tickets)}):\n\n"
            for ticket in tickets:
                result += f"#{ticket.id} - {ticket.title} (Priority: {ticket.priority})\n"
            return result
    except Exception as e:
        return f"Error fetching ticket status: {str(e)}"
    finally:
        db.close()

@tool
def generate_report(report_type: str, title: Optional[str] = None) -> str:
    """Generate a business report based on current data.
    
    Args:
        report_type: Type of report (employee_summary, ticket_summary, department_summary)
        title: Optional custom title for the report
    
    Returns:
        Generated report content
    """
    db = SessionLocal()
    try:
        content = ""
        report_title = title or f"{report_type.replace('_', ' ').title()} - {datetime.now().strftime('%Y-%m-%d')}"
        
        if report_type == "employee_summary":
            total_employees = db.query(Employee).count()
            departments = db.query(Employee.department).distinct().all()
            avg_salary = db.query(Employee).with_entities(Employee.salary).all()
            avg_salary_val = sum([s[0] for s in avg_salary]) / len(avg_salary) if avg_salary else 0
            
            content = (f"Total Employees: {total_employees}\n"
                      f"Departments: {len(departments)}\n"
                      f"Average Salary: ${avg_salary_val:,.2f}\n")
        
        elif report_type == "ticket_summary":
            total_tickets = db.query(Ticket).count()
            open_tickets = db.query(Ticket).filter(Ticket.status == "open").count()
            high_priority = db.query(Ticket).filter(Ticket.priority == "high").count()
            
            content = (f"Total Tickets: {total_tickets}\n"
                      f"Open Tickets: {open_tickets}\n"
                      f"High Priority Tickets: {high_priority}\n")
        
        report = Report(
            title=report_title,
            report_type=report_type,
            content=content,
            generated_by="AI Assistant"
        )
        db.add(report)
        db.commit()
        
        return f"Report Generated: {report_title}\n\n{content}"
    except Exception as e:
        db.rollback()
        return f"Error generating report: {str(e)}"
    finally:
        db.close()

def get_all_tools():
    return [
        create_ticket,
        get_employee_info,
        list_employees,
        get_ticket_status,
        generate_report
    ]
