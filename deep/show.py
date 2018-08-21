#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 15:45:28 2018

@author: van
"""
#import argparse
import sys

from PIL import Image
import tensorflow as tf

tf.reset_default_graph()


def imageprepare(file_name):
    """
    This function returns the pixel values.
    The imput is a png file location.
    """
    #file_name='/home/van/van/1.png'
    #in terminal 'mogrify -format png *.jpg' convert jpg to png
    im = Image.open(file_name).convert('L')
    im=im.resize((28,28),Image.ANTIALIAS)# better output

    #im.save("./sample.png")
    
    tv = list(im.getdata()) #get pixel values

    #normalize pixels to 0 and 1. 0 is pure white, 1 is pure black.
    tva = [ (255-x)*1.0/255.0 for x in tv] 
    #print(tva)
    return tva

def see_by_comp(result):

	"""
	This function returns the predicted integer.
	The imput is the pixel values from the imageprepare() function.
	"""

	# Define the model (same as when creating the model file)

	x = tf.placeholder(tf.float32, [None, 784])
	W = tf.Variable(tf.zeros([784, 10]))
	b = tf.Variable(tf.zeros([10]))

	def weight_variable(shape):
		initial = tf.truncated_normal(shape, stddev=0.1)
		return tf.Variable(initial)

	def bias_variable(shape):
		initial = tf.constant(0.1, shape=shape)
		return tf.Variable(initial)

	def conv2d(x, W):
		return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

	def max_pool_2x2(x):
		return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')   

	W_conv1 = weight_variable([5, 5, 1, 32])
	b_conv1 = bias_variable([32])

	x_image = tf.reshape(x, [-1,28,28,1])
	h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
	h_pool1 = max_pool_2x2(h_conv1)

	W_conv2 = weight_variable([5, 5, 32, 64])
	b_conv2 = bias_variable([64])

	h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
	h_pool2 = max_pool_2x2(h_conv2)

	W_fc1 = weight_variable([7 * 7 * 64, 1024])
	b_fc1 = bias_variable([1024])

	h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
	h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

	keep_prob = tf.placeholder(tf.float32)
	h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

	W_fc2 = weight_variable([1024, 10])
	b_fc2 = bias_variable([10])

	y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

	init_op = tf.global_variables_initializer()



	"""
	Load the model.ckpt file
	file is stored in the same directory as this python script is started
	Use the model to predict the integer. Integer is returend as list.

	Based on the documentatoin at
	https://www.tensorflow.org/versions/master/how_tos/variables/index.html
	"""
	#saver = tf.train.Saver()# This will define the variations twice, making the restore cannot find the model.
	with tf.Session() as sess:
		#tf.reset_default_graph()
		sess.run(init_op)
		#print(restore_vars)
		#all_variables = tf.get_collection_ref(tf.GraphKeys.GLOBAL_VARIABLES)
		#sess.run(tf.variables_initializer(all_variables))
		#saver.restore(sess, "/media/van/D/bigdata/deep/form/model.ckpt")#This always causes some Mistakes like NotFoundError
		saver=tf.train.import_meta_graph('./form/model.ckpt.meta')
		saver.restore(sess, tf.train.latest_checkpoint('./form'))

		#print ("Model restored.")

		prediction=tf.argmax(y_conv,1)
		return prediction.eval(feed_dict={x: [result],keep_prob: 1.0}, session=sess)
		#print(h_conv2)
		#print('recognize result:')
		#print(predint[0])

def main(argv):
	output_image=imageprepare(argv)
	predint=see_by_comp(output_image)
	print('recognize result:')
	print(predint[0])

if __name__=="__main__":
	main(sys.argv[1])
	

