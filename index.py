import pandas as pd
import pyttsx3
import os
import sys

class StudentQueryBot:
    def __init__(self, csv_path="AY26.csv"):
        """Initialize the chatbot"""
        self.csv_path = csv_path
        self.df = None
        self.engine = None
        
        self.load_data()
        self.init_tts()
    
    def load_data(self):
        """Load CSV"""
        try:
            if not os.path.exists(self.csv_path):
                print(f"Error: File '{self.csv_path}' not found!")
                sys.exit(1)
            
            self.df = pd.read_csv(self.csv_path)
            
        except Exception as e:
            print(f"Error loading CSV: {e}")
            sys.exit(1)
    
    def init_tts(self):
        """Initialize text-to-speech"""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 165)
        except:
            self.engine = None
    
    def speak(self, text):
        """Speak text"""
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except:
                pass
    
    def extract_number(self, text):
        """Extract number from text"""
        import re
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else None
    
    def detect_intent(self, question):
        """Detect what user is asking"""
        q = question.lower().strip()
        
        # DISCOUNT queries with numeric conditions (check very early)
        if any(word in q for word in ["more than", "greater than", "above", "zyada", "jyada"]) and any(word in q for word in ["discount", "concession", "chhoot"]):
            return "DISCOUNT_MORE_THAN"
        
        if any(word in q for word in ["less than", "below", "under", "kam", "niche"]) and any(word in q for word in ["discount", "concession", "chhoot"]):
            return "DISCOUNT_LESS_THAN"
        
        if "between" in q and any(word in q for word in ["discount", "concession", "chhoot"]):
            return "DISCOUNT_BETWEEN"
        
        # FEES PAID queries with numeric conditions (check very early)
        if any(word in q for word in ["more than", "greater than", "above", "zyada", "jyada"]) and any(word in q for word in ["paid", "fees", "fee", "payment"]):
            return "FEES_MORE_THAN"
        
        if any(word in q for word in ["less than", "below", "under", "kam", "niche"]) and any(word in q for word in ["paid", "fees", "fee", "payment"]):
            return "FEES_LESS_THAN"
        
        if "between" in q and any(word in q for word in ["paid", "fees", "fee", "payment"]):
            return "FEES_BETWEEN"
        
        # ELIGIBLE queries (check early - specific)
        if any(word in q for word in ["not eligible", "ineligible", "eligible nahi"]):
            return "NOT_ELIGIBLE"
        
        if any(word in q for word in ["eligible", "eligibility"]):
            return "ELIGIBLE"
        
        # BATCH queries (check early)
        if any(word in q for word in ["no batch", "without batch", "batch nahi"]):
            return "NO_BATCH"
        
        if any(word in q for word in ["with batch", "batch assigned", "batch mila", "have batch"]):
            return "WITH_BATCH"
        
        # ADMISSION CANCELLED queries (check first - most specific)
        if any(word in q for word in ["cancelled", "cancel"]) and any(word in q for word in ["admission", "admitted"]):
            return "ADMISSION_CANCELLED"
        
        # ADMISSION queries (check before registration)
        if any(word in q for word in ["admission", "admitted"]):
            return "ADMISSION"
        
        # REGISTRATION queries
        if any(word in q for word in ["registration", "registered", "total", "student", "count", "how many", "kitne"]):
            return "REGISTRATION"
        
        return "UNKNOWN"
    
    def get_registration_students(self):
        """Get students who are actually registered
        Criteria: fees_paid > 3499 AND status = 'Active' AND free_admission = False
        """
        try:
            conditions = (
                (self.df['fees_paid'] > 3499) &
                (self.df['status'] == 'Active') &
                (self.df['free_admission'] == False)
            )
            
            filtered_df = self.df[conditions]
            return len(filtered_df)
            
        except KeyError as e:
            return f"Error: Column {e} not found in data"
        except Exception as e:
            return f"Error: {e}"
    
    def get_admission_students(self):
        """Get students who have admission
        Criteria: Registration criteria + ay26_enrollment_status contains 'Admission'
        """
        try:
            conditions = (
                (self.df['fees_paid'] > 3499) &
                (self.df['status'] == 'Active') &
                (self.df['free_admission'] == False) &
                (self.df['ay26_enrollment_status'].str.contains('Admission', case=False, na=False))
            )
            
            filtered_df = self.df[conditions]
            return len(filtered_df)
            
        except KeyError as e:
            return f"Error: Column {e} not found in data"
        except Exception as e:
            return f"Error: {e}"
    
    def get_admission_cancelled_students(self):
        """Get students whose admission was cancelled
        Criteria: form_status contains 'Admission' (like 'Admission Cancelled', 'Admission Cancel', etc.)
        """
        try:
            conditions = (
                self.df['form_status'].str.contains('Admission', case=False, na=False)
            )
            
            filtered_df = self.df[conditions]
            return len(filtered_df)
            
        except KeyError as e:
            return f"Error: Column {e} not found in data"
        except Exception as e:
            return f"Error: {e}"
    
    def get_no_batch_students(self):
        """Get students without batch
        Criteria: batch contains 'No Batch' AND ay26_enrollment_status contains 'Admission'
        """
        try:
            conditions = (
                (self.df['batch'].str.contains('No Batch', case=False, na=False)) &
                (self.df['ay26_enrollment_status'].str.contains('Admission', case=False, na=False))
            )
            
            filtered_df = self.df[conditions]
            return len(filtered_df)
            
        except KeyError as e:
            return f"Error: Column {e} not found in data"
        except Exception as e:
            return f"Error: {e}"
    
    def get_with_batch_students(self):
        """Get students with batch assigned
        Criteria: batch does NOT contain 'No Batch' AND ay26_enrollment_status contains 'Admission'
        """
        try:
            conditions = (
                (~self.df['batch'].str.contains('No Batch', case=False, na=False)) &
                (self.df['batch'].notna()) &
                (self.df['batch'] != '') &
                (self.df['ay26_enrollment_status'].str.contains('Admission', case=False, na=False))
            )
            
            filtered_df = self.df[conditions]
            return len(filtered_df)
            
        except KeyError as e:
            return f"Error: Column {e} not found in data"
        except Exception as e:
            return f"Error: {e}"
    
    def get_eligible_students(self):
        """Get eligible students
        Criteria: Registration criteria + eligibility_status = 'Eligible'
        """
        try:
            conditions = (
                (self.df['fees_paid'] > 3499) &
                (self.df['status'] == 'Active') &
                (self.df['free_admission'] == False) &
                (self.df['eligibility_status'] == 'Eligible')
            )
            
            filtered_df = self.df[conditions]
            return len(filtered_df)
            
        except KeyError as e:
            return f"Error: Column {e} not found in data"
        except Exception as e:
            return f"Error: {e}"
    
    def get_not_eligible_students(self):
        """Get not eligible students
        Criteria: Registration criteria + eligibility_status != 'Eligible'
        """
        try:
            conditions = (
                (self.df['fees_paid'] > 3499) &
                (self.df['status'] == 'Active') &
                (self.df['free_admission'] == False) &
                (self.df['eligibility_status'] != 'Eligible')
            )
            
            filtered_df = self.df[conditions]
            return len(filtered_df)
            
        except KeyError as e:
            return f"Error: Column {e} not found in data"
        except Exception as e:
            return f"Error: {e}"
    
    def get_fees_more_than(self, amount):
        """Get students who paid more than specified amount"""
        try:
            conditions = (
                self.df['fees_paid'] > amount
            )
            
            filtered_df = self.df[conditions]
            count = len(filtered_df)
            total_amount = filtered_df['fees_paid'].sum()
            
            return {
                'count': count,
                'total': total_amount
            }
            
        except KeyError as e:
            return f"Error: Column {e} not found in data"
        except Exception as e:
            return f"Error: {e}"
    
    def get_fees_less_than(self, amount):
        """Get students who paid less than specified amount"""
        try:
            conditions = (
                self.df['fees_paid'] < amount
            )
            
            filtered_df = self.df[conditions]
            count = len(filtered_df)
            total_amount = filtered_df['fees_paid'].sum()
            
            return {
                'count': count,
                'total': total_amount
            }
            
        except KeyError as e:
            return f"Error: Column {e} not found in data"
        except Exception as e:
            return f"Error: {e}"
    
    def get_fees_between(self, min_amount, max_amount):
        """Get students who paid between specified amounts"""
        try:
            conditions = (
                (self.df['fees_paid'] >= min_amount) &
                (self.df['fees_paid'] <= max_amount)
            )
            
            filtered_df = self.df[conditions]
            count = len(filtered_df)
            total_amount = filtered_df['fees_paid'].sum()
            
            return {
                'count': count,
                'total': total_amount
            }
            
        except KeyError as e:
            return f"Error: Column {e} not found in data"
        except Exception as e:
            return f"Error: {e}"
    
    def get_discount_more_than(self, percentage):
        """Get students who got discount more than specified percentage"""
        try:
            conditions = (
                self.df['% discount'] > percentage
            )
            
            filtered_df = self.df[conditions]
            count = len(filtered_df)
            avg_discount = filtered_df['% discount'].mean()
            
            return {
                'count': count,
                'avg_discount': avg_discount
            }
            
        except KeyError as e:
            return f"Error: Column '% discount' not found in data"
        except Exception as e:
            return f"Error: {e}"
    
    def get_discount_less_than(self, percentage):
        """Get students who got discount less than specified percentage"""
        try:
            conditions = (
                self.df['% discount'] < percentage
            )
            
            filtered_df = self.df[conditions]
            count = len(filtered_df)
            avg_discount = filtered_df['% discount'].mean()
            
            return {
                'count': count,
                'avg_discount': avg_discount
            }
            
        except KeyError as e:
            return f"Error: Column '% discount' not found in data"
        except Exception as e:
            return f"Error: {e}"
    
    def get_discount_between(self, min_percentage, max_percentage):
        """Get students who got discount between specified percentages"""
        try:
            conditions = (
                (self.df['% discount'] >= min_percentage) &
                (self.df['% discount'] <= max_percentage)
            )
            
            filtered_df = self.df[conditions]
            count = len(filtered_df)
            avg_discount = filtered_df['% discount'].mean()
            
            return {
                'count': count,
                'avg_discount': avg_discount
            }
            
        except KeyError as e:
            return f"Error: Column '% discount' not found in data"
        except Exception as e:
            return f"Error: {e}"
    
    def answer(self, question):
        """Answer the question"""
        try:
            intent = self.detect_intent(question)
            print(f"DEBUG: Detected intent = {intent}")
            
            if intent == "REGISTRATION":
                count = self.get_registration_students()
                
                if isinstance(count, str):  # Error message
                    return count
                
                # Two versions: one for display, one for speech
                display_text = f"Registration Students: {count}\n(Criteria: Fees > 3499, Status Active, Not Free Admission)"
                speech_text = f"Registration Students: {count}"
                
                return {"display": display_text, "speech": speech_text}
            
            if intent == "ADMISSION":
                count = self.get_admission_students()
                
                if isinstance(count, str):  # Error message
                    return count
                
                # Two versions: one for display, one for speech
                display_text = f"Admission Students: {count}\n(Criteria: Registration + ay26_enrollment_status contains 'Admission')"
                speech_text = f"Admission Students: {count}"
                
                return {"display": display_text, "speech": speech_text}
            
            if intent == "ADMISSION_CANCELLED":
                count = self.get_admission_cancelled_students()
                
                if isinstance(count, str):  # Error message
                    return count
                
                # Two versions: one for display, one for speech
                display_text = f"Admission Cancelled Students: {count}\n(Criteria: form_status contains 'Admission')"
                speech_text = f"Admission Cancelled Students: {count}"
                
                return {"display": display_text, "speech": speech_text}
            
            if intent == "NO_BATCH":
                count = self.get_no_batch_students()
                
                if isinstance(count, str):  # Error message
                    return count
                
                # Two versions: one for display, one for speech
                display_text = f"Students Without Batch: {count}\n(Criteria: batch = 'No Batch' + Admission status)"
                speech_text = f"Students Without Batch: {count}"
                
                return {"display": display_text, "speech": speech_text}
            
            if intent == "WITH_BATCH":
                count = self.get_with_batch_students()
                
                if isinstance(count, str):  # Error message
                    return count
                
                # Two versions: one for display, one for speech
                display_text = f"Students With Batch: {count}\n(Criteria: batch assigned + Admission status)"
                speech_text = f"Students With Batch: {count}"
                
                return {"display": display_text, "speech": speech_text}
            
            if intent == "ELIGIBLE":
                count = self.get_eligible_students()
                
                if isinstance(count, str):  # Error message
                    return count
                
                # Two versions: one for display, one for speech
                display_text = f"Eligible Students: {count}\n(Criteria: Registration + eligibility_status = 'Eligible')"
                speech_text = f"Eligible Students: {count}"
                
                return {"display": display_text, "speech": speech_text}
            
            if intent == "NOT_ELIGIBLE":
                count = self.get_not_eligible_students()
                
                if isinstance(count, str):  # Error message
                    return count
                
                # Two versions: one for display, one for speech
                display_text = f"Not Eligible Students: {count}\n(Criteria: Registration + eligibility_status != 'Eligible')"
                speech_text = f"Not Eligible Students: {count}"
                
                return {"display": display_text, "speech": speech_text}
            
            if intent == "FEES_MORE_THAN":
                amount = self.extract_number(question)
                
                if not amount:
                    return "Please specify an amount. Example: 'students who paid more than 5000'"
                
                result = self.get_fees_more_than(amount)
                
                if isinstance(result, str):  # Error message
                    return result
                
                # Two versions: one for display, one for speech
                display_text = f"Students who paid more than Rs {amount}: {result['count']}\nTotal Amount: Rs {result['total']:,.2f}"
                speech_text = f"Students who paid more than {amount} rupees: {result['count']}"
                
                return {"display": display_text, "speech": speech_text}
            
            if intent == "FEES_LESS_THAN":
                amount = self.extract_number(question)
                
                if not amount:
                    return "Please specify an amount. Example: 'students who paid less than 2000'"
                
                result = self.get_fees_less_than(amount)
                
                if isinstance(result, str):  # Error message
                    return result
                
                # Two versions: one for display, one for speech
                display_text = f"Students who paid less than Rs {amount}: {result['count']}\nTotal Amount: Rs {result['total']:,.2f}"
                speech_text = f"Students who paid less than {amount} rupees: {result['count']}"
                
                return {"display": display_text, "speech": speech_text}
            
            if intent == "FEES_BETWEEN":
                import re
                numbers = re.findall(r'\d+', question)
                
                if len(numbers) < 2:
                    return "Please specify two amounts. Example: 'students who paid between 5000 and 10000'"
                
                min_amount = int(numbers[0])
                max_amount = int(numbers[1])
                
                result = self.get_fees_between(min_amount, max_amount)
                
                if isinstance(result, str):  # Error message
                    return result
                
                # Two versions: one for display, one for speech
                display_text = f"Students who paid between Rs {min_amount} and Rs {max_amount}: {result['count']}\nTotal Amount: Rs {result['total']:,.2f}"
                speech_text = f"Students who paid between {min_amount} and {max_amount} rupees: {result['count']}"
                
                return {"display": display_text, "speech": speech_text}
            
            if intent == "DISCOUNT_MORE_THAN":
                percentage = self.extract_number(question)
                
                if not percentage:
                    return "Please specify a percentage. Example: 'students who got discount more than 50'"
                
                result = self.get_discount_more_than(percentage)
                
                if isinstance(result, str):  # Error message
                    return result
                
                # Two versions: one for display, one for speech
                display_text = f"Students who got discount more than {percentage}%: {result['count']}\nAverage Discount: {result['avg_discount']:.2f}%"
                speech_text = f"Students who got discount more than {percentage} percent: {result['count']}"
                
                return {"display": display_text, "speech": speech_text}
            
            if intent == "DISCOUNT_LESS_THAN":
                percentage = self.extract_number(question)
                
                if not percentage:
                    return "Please specify a percentage. Example: 'students who got discount less than 30'"
                
                result = self.get_discount_less_than(percentage)
                
                if isinstance(result, str):  # Error message
                    return result
                
                # Two versions: one for display, one for speech
                display_text = f"Students who got discount less than {percentage}%: {result['count']}\nAverage Discount: {result['avg_discount']:.2f}%"
                speech_text = f"Students who got discount less than {percentage} percent: {result['count']}"
                
                return {"display": display_text, "speech": speech_text}
            
            if intent == "DISCOUNT_BETWEEN":
                import re
                numbers = re.findall(r'\d+', question)
                
                if len(numbers) < 2:
                    return "Please specify two percentages. Example: 'discount between 20 and 50'"
                
                min_percentage = int(numbers[0])
                max_percentage = int(numbers[1])
                
                result = self.get_discount_between(min_percentage, max_percentage)
                
                if isinstance(result, str):  # Error message
                    return result
                
                # Two versions: one for display, one for speech
                display_text = f"Students who got discount between {min_percentage}% and {max_percentage}%: {result['count']}\nAverage Discount: {result['avg_discount']:.2f}%"
                speech_text = f"Students who got discount between {min_percentage} and {max_percentage} percent: {result['count']}"
                
                return {"display": display_text, "speech": speech_text}
            
            if intent == "UNKNOWN":
                return "I didn't understand. Try asking: 'how many students?' or 'admission count'"
            
        except Exception as e:
            return f"Error: {e}"
    
    def run(self):
        """Run chatbot"""
        print("\n" + "="*60)
        print("        Welcome to Physics Wallah")
        print("          Student Query Assistant")
        print("="*60)
        print("\nAvailable Queries:")
        print("  - Registration: 'registration', 'total students'")
        print("  - Admission: 'admission', 'admitted students'")
        print("  - Cancelled: 'admission cancelled'")
        print("  - Batch: 'students with batch', 'students without batch'")
        print("  - Eligibility: 'eligible students', 'not eligible'")
        print("  - Fees: 'fees more than 5000', 'fees less than 2000'")
        print("         'fees between 5000 and 10000'")
        print("  - Discount: 'discount more than 50', 'discount less than 30'")
        print("             'discount between 20 and 60'")
        print("\nType 'exit' to stop")
        print("="*60 + "\n")
        
        while True:
            try:
                question = input("You: ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ["exit", "quit", "bye"]:
                    print("AI: Goodbye!")
                    self.speak("Goodbye!")
                    break
                
                response = self.answer(question)
                
                # Handle dict response (with separate display and speech text)
                if isinstance(response, dict):
                    print(f"AI: {response['display']}\n")
                    self.speak(response['speech'])
                else:
                    print(f"AI: {response}\n")
                    self.speak(response)
                
            except KeyboardInterrupt:
                print("\n\nAI: Goodbye!")
                break


if __name__ == "__main__":
    try:
        bot = StudentQueryBot("Ay26.csv")
        bot.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)