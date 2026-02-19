.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: #f5f5f7;
}

.auth-card {
  width: 100%;
  max-width: 440px;
  background: #ffffff;
  border-radius: 18px;
  padding: 48px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.auth-header {
  text-align: center;
  margin-bottom: 40px;
}

.auth-header h1 {
  font-size: 32px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 8px;
  letter-spacing: -0.5px;
}

.auth-header p {
  font-size: 17px;
  color: #86868b;
  font-weight: 400;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: #1d1d1f;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-group input {
  padding: 12px 16px;
  font-size: 17px;
  border: 1px solid #d2d2d7;
  border-radius: 12px;
  background: #ffffff;
  color: #1d1d1f;
  transition: all 0.2s ease;
  font-family: inherit;
}

.form-group input:focus {
  outline: none;
  border-color: #0071e3;
  box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.1);
}

.form-group input::placeholder {
  color: #86868b;
}

.auth-error {
  padding: 12px 16px;
  background: #ff3b30;
  color: white;
  border-radius: 12px;
  font-size: 15px;
  text-align: center;
}

.auth-button {
  width: 100%;
  padding: 14px 24px;
  font-size: 17px;
  font-weight: 600;
  color: white;
  background: #0071e3;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 8px;
}

.auth-button:hover:not(:disabled) {
  background: #0077ed;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.3);
}

.auth-button:active:not(:disabled) {
  transform: translateY(0);
}

.auth-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.auth-footer {
  margin-top: 32px;
  text-align: center;
  padding-top: 24px;
  border-top: 1px solid #d2d2d7;
}

.auth-footer p {
  font-size: 15px;
  color: #86868b;
}

.auth-link {
  color: #0071e3;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s ease;
}

.auth-link:hover {
  color: #0077ed;
  text-decoration: underline;
}

@media (max-width: 480px) {
  .auth-card {
    padding: 32px 24px;
    border-radius: 16px;
  }

  .auth-header h1 {
    font-size: 28px;
  }
}

