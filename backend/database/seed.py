from datetime import datetime, timedelta
from database.models import Employee, Ticket, Report, SessionLocal, init_db

def seed_demo_data():
    init_db()
    db = SessionLocal()
    
    if db.query(Employee).count() > 0:
        print("Database already seeded. Skipping...")
        db.close()
        return
    
    employees = [
        Employee(
            name="John Smith",
            email="john.smith@company.com",
            department="Engineering",
            position="Senior Software Engineer",
            salary=120000.00,
            hire_date=datetime.utcnow() - timedelta(days=730)
        ),
        Employee(
            name="Sarah Johnson",
            email="sarah.johnson@company.com",
            department="Marketing",
            position="Marketing Manager",
            salary=95000.00,
            hire_date=datetime.utcnow() - timedelta(days=1095)
        ),
        Employee(
            name="Michael Chen",
            email="michael.chen@company.com",
            department="Engineering",
            position="DevOps Engineer",
            salary=110000.00,
            hire_date=datetime.utcnow() - timedelta(days=365)
        ),
        Employee(
            name="Emily Davis",
            email="emily.davis@company.com",
            department="HR",
            position="HR Director",
            salary=105000.00,
            hire_date=datetime.utcnow() - timedelta(days=1460)
        ),
        Employee(
            name="David Wilson",
            email="david.wilson@company.com",
            department="Sales",
            position="Sales Representative",
            salary=85000.00,
            hire_date=datetime.utcnow() - timedelta(days=180)
        ),
        Employee(
            name="Rajesh Kumar",
            email="rajesh.kumar@company.com",
            department="Engineering",
            position="Full Stack Developer",
            salary=115000.00,
            hire_date=datetime.utcnow() - timedelta(days=540)
        ),
        Employee(
            name="Priya Sharma",
            email="priya.sharma@company.com",
            department="Product",
            position="Product Manager",
            salary=130000.00,
            hire_date=datetime.utcnow() - timedelta(days=820)
        ),
        Employee(
            name="Amit Patel",
            email="amit.patel@company.com",
            department="Engineering",
            position="Data Scientist",
            salary=125000.00,
            hire_date=datetime.utcnow() - timedelta(days=640)
        ),
        Employee(
            name="Sneha Reddy",
            email="sneha.reddy@company.com",
            department="Design",
            position="UI/UX Designer",
            salary=90000.00,
            hire_date=datetime.utcnow() - timedelta(days=420)
        ),
        Employee(
            name="Vikram Singh",
            email="vikram.singh@company.com",
            department="Sales",
            position="Sales Manager",
            salary=110000.00,
            hire_date=datetime.utcnow() - timedelta(days=910)
        ),
        Employee(
            name="Ananya Iyer",
            email="ananya.iyer@company.com",
            department="Marketing",
            position="Content Strategist",
            salary=88000.00,
            hire_date=datetime.utcnow() - timedelta(days=290)
        ),
        Employee(
            name="Arjun Gupta",
            email="arjun.gupta@company.com",
            department="Engineering",
            position="DevOps Lead",
            salary=135000.00,
            hire_date=datetime.utcnow() - timedelta(days=1200)
        ),
        Employee(
            name="Kavya Nair",
            email="kavya.nair@company.com",
            department="HR",
            position="HR Specialist",
            salary=82000.00,
            hire_date=datetime.utcnow() - timedelta(days=310)
        ),
        Employee(
            name="Rohit Verma",
            email="rohit.verma@company.com",
            department="Engineering",
            position="Backend Engineer",
            salary=118000.00,
            hire_date=datetime.utcnow() - timedelta(days=450)
        ),
        Employee(
            name="Meera Desai",
            email="meera.desai@company.com",
            department="Engineering",
            position="QA Engineer",
            salary=95000.00,
            hire_date=datetime.utcnow() - timedelta(days=270)
        ),
    ]
    
    tickets = [
        Ticket(
            title="System Performance Issue",
            description="The application is running slow during peak hours",
            status="open",
            priority="high",
            assigned_to="Michael Chen"
        ),
        Ticket(
            title="New Feature Request - Dark Mode",
            description="Users are requesting a dark mode option for the application",
            status="in_progress",
            priority="medium",
            assigned_to="John Smith"
        ),
        Ticket(
            title="Bug: Login Form Validation",
            description="Email validation is not working correctly on the login form",
            status="open",
            priority="high",
            assigned_to="John Smith"
        ),
        Ticket(
            title="Database Migration",
            description="Need to migrate from MySQL to PostgreSQL",
            status="open",
            priority="high",
            assigned_to="Rajesh Kumar"
        ),
        Ticket(
            title="API Rate Limiting",
            description="Implement rate limiting for public API endpoints",
            status="in_progress",
            priority="medium",
            assigned_to="Arjun Gupta"
        ),
        Ticket(
            title="Mobile App Crash",
            description="App crashes on Android 12 devices",
            status="open",
            priority="high",
            assigned_to="Amit Patel"
        ),
        Ticket(
            title="Update Documentation",
            description="Update API documentation with new endpoints",
            status="closed",
            priority="low",
            assigned_to="Ananya Iyer"
        ),
        Ticket(
            title="Payment Gateway Integration",
            description="Integrate Stripe payment gateway",
            status="in_progress",
            priority="high",
            assigned_to="Rohit Verma"
        ),
        Ticket(
            title="UI Redesign Homepage",
            description="Redesign landing page with new brand guidelines",
            status="in_progress",
            priority="medium",
            assigned_to="Sneha Reddy"
        ),
        Ticket(
            title="Performance Testing",
            description="Conduct load testing for 10k concurrent users",
            status="open",
            priority="medium",
            assigned_to="Meera Desai"
        ),
    ]
    
    reports = [
        Report(
            title="Q1 2024 Engineering Report",
            report_type="quarterly",
            content="Engineering team completed 45 features and resolved 120 bugs in Q1 2024.",
            generated_by="system"
        ),
        Report(
            title="Employee Satisfaction Survey 2024",
            report_type="survey",
            content="Overall employee satisfaction score: 8.2/10. Key areas for improvement: work-life balance and career development.",
            generated_by="HR Department"
        ),
        Report(
            title="Sales Performance Q1 2024",
            report_type="quarterly",
            content="Sales team exceeded targets by 15%. Total revenue: $2.5M across all departments.",
            generated_by="Sales Team"
        ),
        Report(
            title="Product Launch Analysis",
            report_type="analysis",
            content="New product achieved 10k users in first month. Positive feedback on UX design.",
            generated_by="Product Team"
        ),
        Report(
            title="System Performance Report",
            report_type="technical",
            content="Average response time: 120ms. Achieved 99.9% uptime this quarter.",
            generated_by="DevOps"
        ),
        Report(
            title="Marketing Campaign Results",
            report_type="marketing",
            content="Email campaign achieved 25% open rate and 5% conversion rate.",
            generated_by="Marketing Team"
        ),
    ]
    
    db.add_all(employees)
    db.add_all(tickets)
    db.add_all(reports)
    db.commit()
    db.close()
    
    print("Demo data seeded successfully!")

if __name__ == "__main__":
    seed_demo_data()
