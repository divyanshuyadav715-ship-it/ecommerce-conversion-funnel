import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze():
    # Load data
    print("Loading data...")
    df = pd.read_csv('ecommerce_events.csv')
    
    # 1. Overall Funnel
    funnel_stages = ['session_start', 'product_view', 'add_to_cart', 'checkout_initiate', 'purchase']
    
    # Count unique sessions per stage
    overall_funnel = df.groupby('event_type')['session_id'].nunique().reindex(funnel_stages).reset_index()
    overall_funnel.columns = ['Stage', 'Users']
    
    # Calculate conversion rates
    overall_funnel['Conversion_Rate_From_Start'] = overall_funnel['Users'] / overall_funnel['Users'].iloc[0] * 100
    overall_funnel['Drop_Off_From_Previous'] = 100 - (overall_funnel['Users'] / overall_funnel['Users'].shift(1) * 100).fillna(100)
    
    print("\n=== Overall Funnel ===")
    print(overall_funnel)
    
    # Visualize Overall Funnel
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Users', y='Stage', data=overall_funnel, palette='Blues_d')
    plt.title('Overall E-Commerce Conversion Funnel')
    plt.xlabel('Number of Sessions')
    plt.ylabel('Funnel Stage')
    for index, row in overall_funnel.iterrows():
        plt.text(row.Users, index, f" {row.Users:,} ({row.Conversion_Rate_From_Start:.1f}%)", color='black', va="center")
    plt.tight_layout()
    plt.savefig('funnel_overall.png')
    plt.close()

    # 2. Funnel by Device
    device_funnel = df.groupby(['device_type', 'event_type'])['session_id'].nunique().unstack().reindex(columns=funnel_stages)
    
    print("\n=== Funnel by Device ===")
    print(device_funnel)
    
    # Calculate checkout to purchase conversion by device
    checkout_to_purchase = (device_funnel['purchase'] / device_funnel['checkout_initiate'] * 100).reset_index()
    checkout_to_purchase.columns = ['Device', 'Checkout_to_Purchase_Conversion_Rate']
    
    print("\n=== Checkout to Purchase Conversion by Device ===")
    print(checkout_to_purchase)

    # Visualize Device Funnel Drop-off at Checkout
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Device', y='Checkout_to_Purchase_Conversion_Rate', data=checkout_to_purchase, palette='muted')
    plt.title('Checkout to Purchase Conversion Rate by Device')
    plt.ylabel('Conversion Rate (%)')
    plt.xlabel('Device Type')
    for index, row in checkout_to_purchase.iterrows():
        plt.text(index, row.Checkout_to_Purchase_Conversion_Rate, f"{row.Checkout_to_Purchase_Conversion_Rate:.1f}%", color='black', ha="center", va="bottom")
    plt.tight_layout()
    plt.savefig('checkout_conversion_by_device.png')
    plt.close()
    
    print("\nAnalysis complete. Visualizations saved as 'funnel_overall.png' and 'checkout_conversion_by_device.png'.")

if __name__ == '__main__':
    analyze()
