import os
import sys
import django

# Setup Django
sys.path.insert(0, '/home/filbe/WorkSpace/Aws-Projects/gaming-app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trivia.settings')
django.setup()

from game.models import Room, Question

# Additional questions to expand the pool
ADDITIONAL_QUESTIONS = {
    'Infrastructure & Cloud': {
        'easy': [
            {'text': 'What is an availability zone?', 'option_a': 'A geographic region containing multiple data centers', 'option_b': 'An isolated data center location within a region', 'option_c': 'A network zone that controls access to resources', 'option_d': 'A time zone used for scheduling maintenance windows', 'correct_answer': 'b'},
            {'text': 'What is serverless computing?', 'option_a': 'Running applications without any servers at all', 'option_b': 'A model where the cloud provider manages servers and you pay per execution', 'option_c': 'Deploying applications to servers without operating systems', 'option_d': 'A server architecture that requires no configuration', 'correct_answer': 'b'},
            {'text': 'What is object storage?', 'option_a': 'Storage optimized for storing programming objects and classes', 'option_b': 'A storage service that stores data as objects with metadata and unique identifiers', 'option_c': 'A database that stores objects in a relational table structure', 'option_d': 'Storage that can only hold image and video files', 'correct_answer': 'b'},
            {'text': 'What is a snapshot in cloud computing?', 'option_a': 'A quick photograph of your infrastructure for documentation', 'option_b': 'A point-in-time copy of data or a volume for backup and recovery', 'option_c': 'A monitoring metric that captures system state every second', 'option_d': 'A network packet capture tool for debugging', 'correct_answer': 'b'},
            {'text': 'What is elastic computing?', 'option_a': 'Computing resources that stretch to accommodate any workload', 'option_b': 'The ability to dynamically scale resources up or down based on demand', 'option_c': 'A type of computing that uses elastic network cables', 'option_d': 'Computing that automatically recovers from failures', 'correct_answer': 'b'},
            {'text': 'What is a bastion host?', 'option_a': 'The most powerful server in a cluster that handles peak loads', 'option_b': 'A hardened server that provides secure access to private network resources', 'option_c': 'A backup host that takes over when the primary fails', 'option_d': 'A host that stores all security certificates and keys', 'correct_answer': 'b'},
            {'text': 'What is cloud bursting?', 'option_a': 'When cloud costs suddenly increase beyond budget', 'option_b': 'Temporarily using cloud resources when on-premises capacity is exceeded', 'option_c': 'A security breach that exposes cloud data', 'option_d': 'Rapidly deploying many instances simultaneously', 'correct_answer': 'b'},
            {'text': 'What is a cloud service model?', 'option_a': 'A pricing model for cloud services', 'option_b': 'The level of abstraction provided by a cloud service like IaaS, PaaS, or SaaS', 'option_c': 'A template for deploying cloud resources', 'option_d': 'A service level agreement between provider and customer', 'correct_answer': 'b'},
            {'text': 'What is multi-tenancy in cloud computing?', 'option_a': 'Running multiple applications on a single server', 'option_b': 'Multiple customers sharing the same infrastructure while keeping data isolated', 'option_c': 'Having multiple cloud accounts for different environments', 'option_d': 'Deploying across multiple cloud providers simultaneously', 'correct_answer': 'b'},
            {'text': 'What is a cloud migration?', 'option_a': 'Moving data between different cloud storage tiers', 'option_b': 'The process of moving applications and data from on-premises to cloud', 'option_c': 'Migrating between different versions of cloud services', 'option_d': 'Moving workloads between availability zones', 'correct_answer': 'b'},
            {'text': 'What is cloud orchestration?', 'option_a': 'Coordinating multiple cloud services to work together automatically', 'option_b': 'Managing cloud costs across multiple accounts', 'option_c': 'Organizing cloud resources into folders and tags', 'option_d': 'Scheduling cloud maintenance windows', 'correct_answer': 'a'},
            {'text': 'What is a cloud gateway?', 'option_a': 'A device or service that connects on-premises infrastructure to cloud services', 'option_b': 'The main entrance to a cloud data center', 'option_c': 'A firewall that protects cloud resources', 'option_d': 'A load balancer for cloud applications', 'correct_answer': 'a'},
            {'text': 'What is cloud elasticity?', 'option_a': 'The flexibility to choose different cloud providers', 'option_b': 'The ability to automatically scale resources to match demand', 'option_c': 'The resilience of cloud services to failures', 'option_d': 'The speed at which cloud resources can be provisioned', 'correct_answer': 'b'},
            {'text': 'What is a cloud endpoint?', 'option_a': 'The final destination of cloud network traffic', 'option_b': 'A URL or connection point for accessing a cloud service', 'option_c': 'The edge of a cloud network closest to users', 'option_d': 'A device that connects to cloud services', 'correct_answer': 'b'},
            {'text': 'What is cloud provisioning?', 'option_a': 'Providing cloud services to customers', 'option_b': 'The process of setting up and configuring cloud resources', 'option_c': 'Allocating budget for cloud spending', 'option_d': 'Granting permissions to cloud users', 'correct_answer': 'b'},
            {'text': 'What is a cloud workload?', 'option_a': 'The amount of work a cloud engineer has to do', 'option_b': 'An application or service running in the cloud', 'option_c': 'The total CPU usage across all cloud resources', 'option_d': 'A unit of measurement for cloud billing', 'correct_answer': 'b'},
            {'text': 'What is cloud redundancy?', 'option_a': 'Unnecessary duplicate cloud resources that waste money', 'option_b': 'Having backup resources to ensure availability if primary resources fail', 'option_c': 'Running the same workload in multiple clouds', 'option_d': 'Storing multiple copies of data for compliance', 'correct_answer': 'b'},
            {'text': 'What is a cloud instance?', 'option_a': 'A single occurrence of using a cloud service', 'option_b': 'A virtual server running in the cloud', 'option_c': 'An example configuration for cloud resources', 'option_d': 'A moment in time when cloud resources are measured', 'correct_answer': 'b'},
            {'text': 'What is cloud latency?', 'option_a': 'The delay between requesting and receiving data from cloud services', 'option_b': 'How long it takes to provision new cloud resources', 'option_c': 'The time difference between cloud regions', 'option_d': 'The age of cloud infrastructure', 'correct_answer': 'a'},
            {'text': 'What is a cloud tenant?', 'option_a': 'A customer or organization using cloud services', 'option_b': 'A temporary cloud resource that expires after a period', 'option_c': 'A cloud service that can be rented by the hour', 'option_d': 'A user account within a cloud platform', 'correct_answer': 'a'},
            {'text': 'What is cloud capacity planning?', 'option_a': 'Planning how much data can be stored in the cloud', 'option_b': 'Forecasting future resource needs to ensure adequate capacity', 'option_c': 'Determining the maximum number of users a cloud app can support', 'option_d': 'Planning which cloud services to use', 'correct_answer': 'b'},
            {'text': 'What is a cloud resource?', 'option_a': 'Documentation and tutorials about cloud services', 'option_b': 'Any computing asset available in the cloud like compute, storage, or network', 'option_c': 'A person with cloud expertise', 'option_d': 'A backup copy of cloud data', 'correct_answer': 'b'},
            {'text': 'What is cloud monitoring?', 'option_a': 'Watching cloud formations in the sky', 'option_b': 'Tracking the performance and health of cloud resources', 'option_c': 'Monitoring cloud spending and costs', 'option_d': 'Supervising cloud engineers', 'correct_answer': 'b'},
            {'text': 'What is a cloud backup?', 'option_a': 'A secondary cloud provider used if the primary fails', 'option_b': 'A copy of data stored in the cloud for disaster recovery', 'option_c': 'A backup power supply for cloud data centers', 'option_d': 'A backup plan for cloud migration', 'correct_answer': 'b'},
            {'text': 'What is cloud automation?', 'option_a': 'Using scripts and tools to perform cloud tasks without manual intervention', 'option_b': 'Automatic billing for cloud services', 'option_c': 'Self-healing cloud infrastructure', 'option_d': 'Automatic updates to cloud services', 'correct_answer': 'a'},
            {'text': 'What is a cloud API?', 'option_a': 'An interface for programmatically interacting with cloud services', 'option_b': 'A cloud service for building APIs', 'option_c': 'An application programming interface hosted in the cloud', 'option_d': 'A tool for testing cloud applications', 'correct_answer': 'a'},
            {'text': 'What is cloud compliance?', 'option_a': 'Following cloud provider terms of service', 'option_b': 'Meeting regulatory and security requirements when using cloud services', 'option_c': 'Ensuring cloud resources comply with budget limits', 'option_d': 'Complying with cloud best practices', 'correct_answer': 'b'},
            {'text': 'What is a cloud dashboard?', 'option_a': 'The front panel of a cloud server', 'option_b': 'A visual interface showing cloud resource status and metrics', 'option_c': 'A car dashboard that connects to cloud services', 'option_d': 'A summary report of cloud usage', 'correct_answer': 'b'},
            {'text': 'What is cloud portability?', 'option_a': 'Using portable devices to access cloud services', 'option_b': 'The ability to move applications between different cloud providers', 'option_c': 'Accessing cloud services from anywhere', 'option_d': 'The lightweight nature of cloud applications', 'correct_answer': 'b'},
            {'text': 'What is a cloud console?', 'option_a': 'A gaming console that streams games from the cloud', 'option_b': 'A web-based interface for managing cloud resources', 'option_c': 'A command-line tool for cloud administration', 'option_d': 'A physical terminal in a cloud data center', 'correct_answer': 'b'},
        ],
        'hard': [
            {'text': 'What is the blast radius in cloud architecture?', 'option_a': 'The geographic area affected by a data center outage', 'option_b': 'The scope of impact when a component or change fails', 'option_c': 'The range of a DDoS attack on cloud infrastructure', 'option_d': 'The number of users affected by a security breach', 'correct_answer': 'b'},
            {'text': 'What is infrastructure drift?', 'option_a': 'The gradual movement of data centers due to tectonic shifts', 'option_b': 'When actual infrastructure configuration diverges from the defined state', 'option_c': 'The slow degradation of infrastructure performance over time', 'option_d': 'When infrastructure costs drift above budget', 'correct_answer': 'b'},
            {'text': 'What is the shared responsibility model?', 'option_a': 'A model where multiple teams share responsibility for infrastructure', 'option_b': 'The division of security responsibilities between cloud provider and customer', 'option_c': 'A cost-sharing model for multi-tenant cloud resources', 'option_d': 'A model where infrastructure responsibilities are shared across regions', 'correct_answer': 'b'},
            {'text': 'What is cloud-native architecture?', 'option_a': 'Architecture designed specifically for a single cloud provider', 'option_b': 'Applications designed to fully leverage cloud capabilities like auto-scaling and microservices', 'option_c': 'Architecture that only uses native cloud services without third-party tools', 'option_d': 'Infrastructure that was born in the cloud rather than migrated', 'correct_answer': 'b'},
            {'text': 'What is the noisy neighbor problem?', 'option_a': 'When monitoring alerts are too frequent and disruptive', 'option_b': 'When one tenant resource usage impacts performance of other tenants on shared infrastructure', 'option_c': 'When network traffic from one service interferes with another', 'option_d': 'When log volume from one application overwhelms the logging system', 'correct_answer': 'b'},
            {'text': 'What is immutable infrastructure?', 'option_a': 'Infrastructure that cannot be changed after deployment and is replaced rather than updated', 'option_b': 'Infrastructure protected by immutable backups', 'option_c': 'Infrastructure that uses immutable storage for data', 'option_d': 'Infrastructure with unchangeable security policies', 'correct_answer': 'a'},
            {'text': 'What is the cattle vs pets analogy in infrastructure?', 'option_a': 'Cattle are production servers while pets are development servers', 'option_b': 'Cattle are disposable identical servers while pets are unique servers that are maintained', 'option_c': 'Cattle are virtual machines while pets are containers', 'option_d': 'Cattle are cloud resources while pets are on-premises resources', 'correct_answer': 'b'},
            {'text': 'What is cloud resource tagging strategy?', 'option_a': 'A strategy for pricing cloud resources', 'option_b': 'A systematic approach to labeling resources for organization, cost allocation, and automation', 'option_c': 'A method for marking resources for deletion', 'option_d': 'A security strategy for identifying sensitive resources', 'correct_answer': 'b'},
            {'text': 'What is the difference between RPO and RTO?', 'option_a': 'RPO is for backups while RTO is for replication', 'option_b': 'RPO is acceptable data loss while RTO is acceptable downtime', 'option_c': 'RPO is for recovery while RTO is for redundancy', 'option_d': 'RPO is measured in bytes while RTO is measured in time', 'correct_answer': 'b'},
            {'text': 'What is cloud cost optimization?', 'option_a': 'Choosing the cheapest cloud provider', 'option_b': 'Strategies to reduce cloud spending while maintaining performance and availability', 'option_c': 'Optimizing applications to use less cloud resources', 'option_d': 'Negotiating better rates with cloud providers', 'correct_answer': 'b'},
        ],
    },
}

def import_questions():
    """Import additional questions into database"""
    total_added = 0
    
    for room_name, difficulties in ADDITIONAL_QUESTIONS.items():
        try:
            room = Room.objects.get(name=room_name)
            print(f"\n🎯 Processing: {room_name}")
            
            for difficulty, questions in difficulties.items():
                added = 0
                for q in questions:
                    _, created = Question.objects.get_or_create(
                        room=room,
                        text=q['text'],
                        difficulty=difficulty,
                        defaults={
                            'option_a': q['option_a'],
                            'option_b': q['option_b'],
                            'option_c': q['option_c'],
                            'option_d': q['option_d'],
                            'correct_answer': q['correct_answer'],
                        }
                    )
                    if created:
                        added += 1
                
                total_added += added
                print(f"   ✅ {difficulty.capitalize()}: Added {added} questions")
                
        except Room.DoesNotExist:
            print(f"   ❌ Room '{room_name}' not found")
    
    print(f"\n✨ Done! Added {total_added} new questions")
    print(f"📊 Total questions in database: {Question.objects.count()}")

if __name__ == '__main__':
    import_questions()
