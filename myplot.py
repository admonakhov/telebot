import matplotlib.pyplot as plt
deafault_user ={
    'line': '',
    'dots': '',
    'color': ''

}
def plot(X, Y, usr=deafault_user):
    plt.plot(X, Y, 'ro')
    plt.grid()
    plt.savefig('tmp.png')
    plt.close()