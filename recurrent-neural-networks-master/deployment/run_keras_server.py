from utils import generate_random_start
#import tensorflow as tf
from flask import Flask, render_template, request
from wtforms import Form, StringField, validators, SubmitField, DecimalField, IntegerField

# Create app
app = Flask(__name__)


class ReusableForm(Form):
    """User entry form for entering specifics for generation"""
    # Starting seed
    seed = StringField("Enter the name of Job Position or type 'random':", validators=[
                     validators.InputRequired()])
    # Number of words
    words = IntegerField('Enter the Job index to match against:',
                         default=0, validators=[validators.InputRequired(),
                                                 validators.NumberRange(min=0, max=24, message='Index must be between 0 and 24')])
    # Submit button
    submit = SubmitField("Enter")


'''def load_keras_model():
    """Load in the pre-trained model"""
    global model
    model = load_model('../models/train-embeddings-rnn.h5')
    # Required for model to work
    global graph
    graph = tf.get_default_graph()
'''

# Home page
@app.route("/", methods=['GET', 'POST'])
def home():
    """Home page of app with form"""
    # Create form
    form = ReusableForm(request.form)

    # On form entry and all conditions met
    if request.method == 'POST' and form.validate():
        # Extract information
        seed = request.form['seed']
        #diversity = float(request.form['diversity'])
        words = int(request.form['words'])
        # Generate a random sequence
        if seed == 'random':
            return render_template('random.html', input=generate_random_start(index=words))
        # Generate starting from a seed sequence
        else:
            return render_template('random.html', input=generate_random_start(index=words))
    # Send template information to index.html
    return render_template('index.html', form=form)


if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    #load_keras_model()
    # Run app
    app.run(host="0.0.0.0", port=80)
