// pipeline {
//     agent any

//     stages {
//         stage('Install') {
//             steps {
//                 sh 'python -m pip install -r requirements.txt'
//             }
//         }

//         stage('Test') {
//             steps {
//                 sh 'mkdir -p reports'
//                 sh 'pytest'
//             }
//         }
//     }

//     post {
//         always {
//             junit testResults: 'reports/junit.xml', allowEmptyResults: true
//             archiveArtifacts artifacts: 'reports/*', onlyIfSuccessful: false
//             sh 'python scripts/notify_feishu.py'
//         }
//     }
// }

pipeline {
    agent any

    environment {
        FEISHU_WEBHOOK = 'https://open.feishu.cn/open-apis/bot/v2/hook/27afc8b5-1b76-44f6-b3e8-75f7e604bf04000'
    }

    stages {
        stage('Checkout') {
            steps {
                echo '拉取代码...'
                checkout scm
            }
        }

        stage('Install') {
            steps {
                echo '安装依赖...'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo '执行测试...'
                sh 'pytest tests/ -v --tb=short 2>&1 | tee test_result.txt'
            }
        }
    }

    post {
        success {
            script {
                sendFeishu("✅ 测试通过", "SUCCESS")
            }
        }
        failure {
            script {
                sendFeishu("❌ 测试失败", "FAILURE")
            }
        }
        always {
            echo '流水线执行完毕'
        }
    }
}

def sendFeishu(String title, String status) {
    def color = status == 'SUCCESS' ? 'green' : 'red'
    def body = """{
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "${title}"
                },
                "template": "${color}"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "**项目：** ${env.JOB_NAME}\\n**分支：** ${env.GIT_BRANCH ?: 'main'}\\n**构建号：** #${env.BUILD_NUMBER}\\n**耗时：** ${currentBuild.durationString}"
                    }
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "查看构建日志"
                            },
                            "url": "${env.BUILD_URL}",
                            "type": "default"
                        }
                    ]
                }
            ]
        }
    }"""

    sh """
        curl -s -X POST '${FEISHU_WEBHOOK}' \\
        -H 'Content-Type: application/json' \\
        -d '${body}'
    """
}
