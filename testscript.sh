python3 -m venv .venv                                                                                                         
source .venv/bin/activate                                                                                                     
                                                                                                                                
  # Install dependencies (use pip3 or python -m pip)                                                                            
python3 -m pip install -r requirements.txt                                                                                    
                                                                                                                                
  # Run the chatbot                                                                                                             
PYTHONPATH=. python3 -m chatbot.main 
