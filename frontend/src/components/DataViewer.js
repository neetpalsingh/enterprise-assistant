import React, { useState, useEffect } from 'react';
import { X, Sun, Moon, Users, Ticket, FileText, RefreshCw } from 'lucide-react';
import { motion } from 'framer-motion';
import axios from 'axios';
import './DataViewer.css';

const DataViewer = ({ theme, toggleTheme, onClose }) => {
  const [data, setData] = useState({ employees: [], tickets: [], reports: [] });
  const [activeTab, setActiveTab] = useState('employees');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [employeesRes, ticketsRes, reportsRes] = await Promise.all([
        axios.get('http://localhost:8002/employees'),
        axios.get('http://localhost:8002/tickets'),
        axios.get('http://localhost:8002/reports')
      ]);

      setData({
        employees: employeesRes.data.map(emp => ({
          name: emp.name,
          email: emp.email,
          position: emp.position,
          department: emp.department,
          salary: `$${emp.salary.toLocaleString()}`
        })),
        tickets: ticketsRes.data.map(ticket => ({
          id: ticket.id,
          title: ticket.title,
          status: ticket.status,
          priority: ticket.priority,
          assigned: ticket.assigned_to
        })),
        reports: reportsRes.data.map(report => ({
          title: report.title,
          type: report.report_type,
          date: new Date(report.created_at).toLocaleDateString()
        }))
      });
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="data-viewer">
      <div className={`data-container glass-${theme}`}>
        <div className="data-header">
          <div className="header-left">
            <FileText size={24} />
            <h1>Database Viewer</h1>
          </div>
          <div className="header-actions">
            <button onClick={fetchData} className="icon-btn" disabled={loading}>
              <RefreshCw size={20} className={loading ? 'spin' : ''} />
            </button>
            <button onClick={toggleTheme} className="icon-btn">
              {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
            </button>
            <button onClick={onClose} className="icon-btn">
              <X size={20} />
            </button>
          </div>
        </div>

        <div className="data-tabs">
          <button
            onClick={() => setActiveTab('employees')}
            className={`tab ${activeTab === 'employees' ? 'active' : ''}`}
          >
            <Users size={18} />
            Employees ({data.employees.length})
          </button>
          <button
            onClick={() => setActiveTab('tickets')}
            className={`tab ${activeTab === 'tickets' ? 'active' : ''}`}
          >
            <Ticket size={18} />
            Tickets ({data.tickets.length})
          </button>
          <button
            onClick={() => setActiveTab('reports')}
            className={`tab ${activeTab === 'reports' ? 'active' : ''}`}
          >
            <FileText size={18} />
            Reports ({data.reports.length})
          </button>
        </div>

        <div className="data-content">
          {activeTab === 'employees' && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Position</th>
                    <th>Department</th>
                    <th>Salary</th>
                  </tr>
                </thead>
                <tbody>
                  {data.employees.map((emp, idx) => (
                    <tr key={idx}>
                      <td>{emp.name}</td>
                      <td>{emp.email}</td>
                      <td>{emp.position}</td>
                      <td>{emp.department}</td>
                      <td className="salary">{emp.salary}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </motion.div>
          )}

          {activeTab === 'tickets' && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Status</th>
                    <th>Priority</th>
                    <th>Assigned To</th>
                  </tr>
                </thead>
                <tbody>
                  {data.tickets.map((ticket, idx) => (
                    <tr key={idx}>
                      <td>#{ticket.id}</td>
                      <td>{ticket.title}</td>
                      <td><span className={`status ${ticket.status}`}>{ticket.status}</span></td>
                      <td><span className={`badge ${ticket.priority}`}>{ticket.priority}</span></td>
                      <td>{ticket.assigned}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </motion.div>
          )}

          {activeTab === 'reports' && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Title</th>
                    <th>Type</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {data.reports.map((report, idx) => (
                    <tr key={idx}>
                      <td>{report.title}</td>
                      <td><span className="badge">{report.type}</span></td>
                      <td>{report.date}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DataViewer;
