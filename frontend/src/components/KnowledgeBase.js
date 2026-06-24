import React, { useState, useEffect } from 'react';
import { Upload, FileText, Trash2, CheckCircle, Clock, X, RefreshCw } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import './KnowledgeBase.css';

const API_BASE = 'http://localhost:8002';

const DOCUMENT_TYPES = [
  { value: 'policy', label: 'Policy' },
  { value: 'compliance', label: 'Compliance' },
  { value: 'finance', label: 'Finance' },
  { value: 'contract', label: 'Contract' },
  { value: 'hr', label: 'HR' },
  { value: 'technical', label: 'Technical' },
  { value: 'basic', label: 'Basic' }
];

const KnowledgeBase = ({ theme, onClose }) => {
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [processing, setProcessing] = useState({});
  const [selectedType, setSelectedType] = useState('basic');
  const [message, setMessage] = useState(null);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const response = await axios.get(`${API_BASE}/knowledge/documents`);
      setDocuments(response.data);
    } catch (error) {
      console.error('Error loading documents:', error);
      showMessage('Failed to load documents', 'error');
    }
  };

  const showMessage = (text, type = 'success') => {
    setMessage({ text, type });
    setTimeout(() => setMessage(null), 3000);
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', selectedType);

    setUploading(true);
    try {
      const response = await axios.post(`${API_BASE}/knowledge/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      showMessage(response.data.message, 'success');
      loadDocuments();
    } catch (error) {
      showMessage(error.response?.data?.detail || 'Upload failed', 'error');
    } finally {
      setUploading(false);
      event.target.value = '';
    }
  };

  const handleProcess = async (docId) => {
    setProcessing(prev => ({ ...prev, [docId]: true }));
    try {
      const response = await axios.post(`${API_BASE}/knowledge/process/${docId}`);
      showMessage(response.data.message, 'success');
      loadDocuments();
    } catch (error) {
      showMessage(error.response?.data?.detail || 'Processing failed', 'error');
    } finally {
      setProcessing(prev => ({ ...prev, [docId]: false }));
    }
  };

  const handleDelete = async (docId) => {
    if (!window.confirm('Delete this document? This will remove it from the knowledge base.')) {
      return;
    }

    try {
      await axios.delete(`${API_BASE}/knowledge/documents/${docId}`);
      showMessage('Document deleted', 'success');
      loadDocuments();
    } catch (error) {
      showMessage(error.response?.data?.detail || 'Delete failed', 'error');
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <div className={`knowledge-base ${theme}`}>
      <div className={`kb-header glass-${theme}`}>
        <div className="header-left">
          <FileText size={24} />
          <h2>Knowledge Base</h2>
        </div>
        <button onClick={onClose} className="close-btn" title="Close">
          <X size={20} />
        </button>
      </div>

      {message && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className={`message ${message.type}`}
        >
          {message.text}
        </motion.div>
      )}

      <div className="kb-content">
        <div className={`upload-section glass-${theme}`}>
          <h3>Upload Document</h3>
          <div className="upload-controls">
            <select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
              className={`type-select ${theme}`}
            >
              {DOCUMENT_TYPES.map(type => (
                <option key={type.value} value={type.value}>
                  {type.label}
                </option>
              ))}
            </select>

            <label className={`upload-btn ${uploading ? 'uploading' : ''}`}>
              <Upload size={18} />
              {uploading ? 'Uploading...' : 'Choose File'}
              <input
                type="file"
                accept=".pdf,.docx,.doc"
                onChange={handleFileUpload}
                disabled={uploading}
                style={{ display: 'none' }}
              />
            </label>

            <button onClick={loadDocuments} className="refresh-btn" title="Refresh">
              <RefreshCw size={18} />
            </button>
          </div>
          <p className="file-info">Supported: PDF, DOCX, DOC</p>
        </div>

        <div className="documents-list">
          <AnimatePresence>
            {documents.map(doc => (
              <motion.div
                key={doc.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, x: -100 }}
                className={`document-card glass-${theme}`}
              >
                <div className="doc-icon">
                  <FileText size={32} />
                </div>
                <div className="doc-info">
                  <h4>{doc.file_name}</h4>
                  <div className="doc-meta">
                    <span className={`doc-type ${doc.document_type}`}>
                      {doc.document_type}
                    </span>
                    <span className="doc-size">{formatFileSize(doc.size)}</span>
                    {doc.processed && (
                      <span className="doc-chunks">{doc.chunks} chunks</span>
                    )}
                  </div>
                </div>
                <div className="doc-actions">
                  {doc.processed ? (
                    <div className="status-badge processed">
                      <CheckCircle size={16} />
                      Processed
                    </div>
                  ) : (
                    <button
                      onClick={() => handleProcess(doc.id)}
                      disabled={processing[doc.id]}
                      className="process-btn"
                    >
                      {processing[doc.id] ? (
                        <>
                          <Clock size={16} className="spin" />
                          Processing...
                        </>
                      ) : (
                        <>
                          <CheckCircle size={16} />
                          Process
                        </>
                      )}
                    </button>
                  )}
                  <button
                    onClick={() => handleDelete(doc.id)}
                    className="delete-btn"
                    title="Delete"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {documents.length === 0 && (
            <div className="empty-state">
              <FileText size={48} />
              <p>No documents uploaded yet</p>
              <p className="hint">Upload documents to build your knowledge base</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default KnowledgeBase;
