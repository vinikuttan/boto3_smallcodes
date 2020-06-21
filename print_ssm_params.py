import boto3                                                                                           
import os                                                                                              
import sys                                                                                             
                                                                                                       
env  = sys.argv[1]                                                                                     
params = []                                                                                            
                                                                                                       
key_id = '************************************'                                                        
secret_key = '********************************'                                                        
region = '******'                                                                                      
client= boto3.client('ssm', region, aws_access_key_id=key_id, aws_secret_access_key=secret_key)        
                                                                                                       
def fetch_paramters(next_token='', attempts=0):                                                        
    """ fetch the paramaters in iteration from ssm paramter store with nested token"""                 
                                                                                                       
    if attempts and not next_token:                                                                    
        return []                                                                                      
    if attempts:                                                                                       
        response = client.get_parameters_by_path(Path='/'+ env + '/' , NextToken=next_token, Recursive=True, WithDecryption=True)
    else:                                                                                              
        response = client.get_parameters_by_path(Path='/'+ env + '/' , Recursive=True, WithDecryption=True)
                                                                                                       
    attempts += 1                                                                                      
    # max nested to 10                                                                                 
    if attempts < 11:                                                                                  
        params.extend(fetch_paramters(next_token=response.get('NextToken'), attempts=attempts))        
                                                                                                       
    return response.get('Parameters', [])                                                              
                                                                                                       
                                                                                                       
fetch_paramters()                                                                                      
export_stmt = []                                                                                       
for each in params:                                                                                    
    export_stmt.append('export '+ each['Name'].split('/')[2] + '=' + each['Value'])                    
                                                                                                                                                                                                                                                 
print("\n".join(export_stmt))
