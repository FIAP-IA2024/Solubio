import boto3

def calculate_twilio_costs(conversations, total_messages, exchange_rate):
    # Custos da Twilio para conversas utilitárias no Brasil
    cost_per_conversation = 0.008 * exchange_rate  # Custo por conversa em R$ (ajustado com taxa de câmbio)
    cost_per_message = 0.005 * exchange_rate       # Custo por mensagem em R$ (ajustado com taxa de câmbio)
    
    conversation_cost = conversations * cost_per_conversation
    message_cost = total_messages * cost_per_message
    total_twilio_cost = conversation_cost + message_cost
    
    return {
        "Twilio (Custo por Conversas)": (conversation_cost, f"Conversas: {conversations} * Custo por conversa: R${cost_per_conversation:.4f}"),
        "Twilio (Custo por Mensagens)": (message_cost, f"Total de mensagens: {total_messages} * Custo por mensagem: R${cost_per_message:.4f}"),
        "Total Twilio": total_twilio_cost
    }

def calculate_aws_costs(api_calls, ec2_hours, storage_gb, dynamo_read_write_units, sagemaker_hours, nat_gb, exchange_rate):
    # Estimativas de custo AWS na região de São Paulo - valores em reais
    cost_per_api_call = 0.000005 * exchange_rate  # Exemplo para chamadas no API Gateway
    cost_per_ec2_hour = 0.15 * exchange_rate      # Exemplo de custo por hora da instância EC2
    cost_per_gb_storage = 0.04 * exchange_rate    # Exemplo de custo por GB no S3
    cost_per_dynamo_read_write_unit = 0.003 * exchange_rate  # Exemplo para DynamoDB
    cost_per_sagemaker_hour = 13.0 * exchange_rate  # Exemplo para uso de SageMaker
    cost_per_nat_gb = 0.07 * exchange_rate  # Custo por GB de transferência via NAT Gateway
    
    # Cálculos de custo de cada componente
    api_cost = api_calls * cost_per_api_call
    ec2_cost = ec2_hours * cost_per_ec2_hour
    storage_cost = storage_gb * cost_per_gb_storage
    dynamo_cost = dynamo_read_write_units * cost_per_dynamo_read_write_unit
    sagemaker_cost = sagemaker_hours * cost_per_sagemaker_hour
    nat_cost = nat_gb * cost_per_nat_gb
    
    total_aws_cost = api_cost + ec2_cost + storage_cost + dynamo_cost + sagemaker_cost + nat_cost
    
    return {
        "API Gateway": (api_cost, f"Chamadas API: {api_calls} * Custo por chamada: R${cost_per_api_call:.6f}"),
        "EC2 (Instâncias)": (ec2_cost, f"Horas EC2: {ec2_hours} * Custo por hora: R${cost_per_ec2_hour:.2f}"),
        "S3 (Armazenamento)": (storage_cost, f"Armazenamento S3: {storage_gb} GB * Custo por GB: R${cost_per_gb_storage:.2f}"),
        "DynamoDB": (dynamo_cost, f"Unidades de leitura/escrita: {dynamo_read_write_units} * Custo por unidade: R${cost_per_dynamo_read_write_unit:.3f}"),
        "SageMaker": (sagemaker_cost, f"Horas SageMaker: {sagemaker_hours} * Custo por hora: R${cost_per_sagemaker_hour:.2f}"),
        "NAT Gateway": (nat_cost, f"Transferência NAT: {nat_gb} GB * Custo por GB: R${cost_per_nat_gb:.2f}"),
        "Total AWS": total_aws_cost
    }

def main():
    print("Estimação de Custos da Solução de Chatbot (Região: São Paulo - AWS sa-east-1)")
    
    # Taxa de câmbio
    exchange_rate = float(input("Informe a taxa de câmbio atual (USD para BRL): "))
    
    # Inputs de mensagem para Twilio
    conversations = int(input("Número de conversas (24 horas cada): "))
    total_messages = int(input("Número total de mensagens trocadas: "))
    
    # Inputs de uso AWS
    api_calls = int(input("Número de chamadas na API Gateway: "))
    ec2_hours = float(input("Horas de uso de instância EC2: "))
    storage_gb = float(input("Armazenamento em S3 (GB): "))
    dynamo_read_write_units = int(input("Unidades de leitura/escrita DynamoDB: "))
    sagemaker_hours = float(input("Horas de uso do SageMaker: "))
    nat_gb = float(input("Transferência de dados via NAT Gateway (GB): "))
    
    # Cálculo dos custos
    twilio_costs = calculate_twilio_costs(conversations, total_messages, exchange_rate)
    aws_costs = calculate_aws_costs(api_calls, ec2_hours, storage_gb, dynamo_read_write_units, sagemaker_hours, nat_gb, exchange_rate)
    
    total_cost = twilio_costs["Total Twilio"] + aws_costs["Total AWS"]
    
    print("\n*** Estimativa de Custos Detalhada ***")
    
    # Exibindo os custos do Twilio com explicações
    print("\n--- Custos Twilio ---")
    for key, value in twilio_costs.items():
        if isinstance(value, tuple):
            cost, explanation = value
            print(f"{key}: R${cost:.2f} ({explanation})")
        else:
            print(f"{key}: R${value:.2f}")
    
    # Exibindo os custos da AWS com explicações
    print("\n--- Custos AWS ---")
    for key, value in aws_costs.items():
        if isinstance(value, tuple):
            cost, explanation = value
            print(f"{key}: R${cost:.2f} ({explanation})")
        else:
            print(f"{key}: R${value:.2f}")
    
    # Exibindo o custo total
    print("\n*** Custo Total da Solução ***")
    print(f"Custo Total: R${total_cost:.2f}")

# Chamando a função principal
if __name__ == "__main__":
    main()

