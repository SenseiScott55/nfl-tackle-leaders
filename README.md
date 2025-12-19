# NFL Weekly Tackle Leaders Tracker

Automated serverless data pipeline that tracks NFL weekly leaders in Total Tackles and Tackles for Loss.

## Architecture

[Architecture diagram will go here]

## Tech Stack

- **Infrastructure as Code:** Terraform with modular design
- **Compute:** AWS Lambda (Python 3.11)
- **Storage:** DynamoDB
- **API:** API Gateway (REST)
- **Frontend:** S3 Static Website
- **Orchestration:** EventBridge (CloudWatch Events)
- **Monitoring:** CloudWatch Logs
- **State Management:** S3 backend with DynamoDB locking
- **Version Control:** GitHub

## Features

- Automated weekly data collection (every Tuesday)
- Tracks top player in Total Tackles per week
- Tracks top player in Tackles for Loss per week
- REST API for data access
- Interactive web dashboard
- Historical data for 2024 NFL season
- Infrastructure as Code (100% Terraform)

##  Project Goals

This project demonstrates:
- Serverless architecture design
- Infrastructure as Code best practices
- Python data processing
- AWS service integration
- API design
- Frontend development
- Cost-conscious cloud engineering

##  Cost Estimate

**Monthly Cost: < $1**
- DynamoDB: Free tier (~36 items)
- Lambda: Free tier (~4 invocations/month)
- API Gateway: Free tier
- S3: ~$0.50
- CloudWatch: Free tier





## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 👤 Author

[Your Name]
- GitHub: [SenseiScott55]
- LinkedIn: [https://www.linkedin.com/in/hunter-scott-158249243/]
