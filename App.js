.App {
  min-height: 100vh;
  background: #f5f5f7;
  display: flex;
  flex-direction: column;
}

.app-content {
  flex: 1;
  display: flex;
  justify-content: center;
  padding: 40px 20px;
}

.container {
  background: #ffffff;
  border-radius: 20px;
  max-width: 1200px;
  width: 100%;
  padding: 60px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.app-header {
  text-align: center;
  margin-bottom: 60px;
  padding-bottom: 40px;
  border-bottom: 1px solid #d2d2d7;
}

.app-header h1 {
  font-size: 56px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 12px;
  letter-spacing: -1.5px;
  line-height: 1.1;
}

.app-header p {
  font-size: 21px;
  color: #86868b;
  font-weight: 400;
  line-height: 1.5;
}

.main-content {
  margin-top: 40px;
}

.tab-selector {
  display: flex;
  gap: 0;
  margin-bottom: 40px;
  background: #f5f5f7;
  border-radius: 12px;
  padding: 4px;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.tab-button {
  flex: 1;
  padding: 12px 24px;
  background: transparent;
  border: none;
  border-radius: 10px;
  font-size: 17px;
  font-weight: 400;
  color: #86868b;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.tab-button:hover {
  color: #1d1d1f;
}

.tab-button.active {
  color: #1d1d1f;
  background: #ffffff;
  font-weight: 500;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.tab-content {
  min-height: 300px;
}

.error-message {
  margin-top: 24px;
  padding: 16px 20px;
  background: #ff3b30;
  color: white;
  border-radius: 12px;
  text-align: center;
  font-size: 15px;
  font-weight: 400;
}

.error-message p {
  margin: 0;
}

@media (max-width: 768px) {
  .app-content {
    padding: 20px 16px;
  }

  .container {
    padding: 40px 24px;
    border-radius: 16px;
  }

  .app-header {
    margin-bottom: 40px;
    padding-bottom: 30px;
  }

  .app-header h1 {
    font-size: 40px;
  }

  .app-header p {
    font-size: 19px;
  }

  .tab-selector {
    max-width: 100%;
  }

  .tab-button {
    font-size: 15px;
    padding: 10px 20px;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 32px 20px;
  }

  .app-header h1 {
    font-size: 32px;
  }

  .app-header p {
    font-size: 17px;
  }
}
