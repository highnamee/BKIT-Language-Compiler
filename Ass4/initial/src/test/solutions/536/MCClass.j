.source MCClass.java
.class public MCClass
.super java.lang.Object

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
.var 1 is x [I from Label0 to Label1
	iconst_5
	newarray int
	dup
	iconst_0
	iconst_1
	iastore
	dup
	iconst_1
	iconst_5
	iastore
	dup
	iconst_2
	iconst_2
	iastore
	dup
	iconst_3
	bipush 7
	iastore
	dup
	iconst_4
	iconst_4
	iastore
	astore_1
Label0:
	aload_1
	invokestatic MCClass/bubbleSort([I)V
Label1:
	return
.limit stack 4
.limit locals 2
.end method

.method public static bubbleSort([I)V
.var 0 is x [I from Label0 to Label1
.var 1 is iter I from Label0 to Label1
	iconst_0
	istore_1
.var 2 is innerIter I from Label0 to Label1
	iconst_0
	istore_2
Label0:
	iconst_0
	istore_1
Label4:
	iload_1
	iconst_5
	if_icmpge Label5
	iconst_1
	goto Label6
Label5:
	iconst_0
Label6:
	ifle Label3
	iload_1
	istore_2
Label9:
	iload_2
	iconst_5
	if_icmpge Label10
	iconst_1
	goto Label11
Label10:
	iconst_0
Label11:
	ifle Label8
	aload_0
	iload_1
	iaload
	aload_0
	iload_2
	iaload
	if_icmple Label14
	iconst_1
	goto Label15
Label14:
	iconst_0
Label15:
	ifle Label12
.var 3 is temp I from Label0 to Label1
	iconst_0
	istore_3
	aload_0
	iload_1
	iaload
	istore_3
	aload_0
	iload_1
	aload_0
	iload_2
	iaload
	iastore
	aload_0
	iload_2
	iload_3
	iastore
	goto Label13
Label12:
Label13:
Label7:
	iload_2
	iconst_1
	iadd
	istore_2
	goto Label9
Label8:
Label2:
	iload_1
	iconst_1
	iadd
	istore_1
	goto Label4
Label3:
	iconst_0
	istore_1
Label18:
	iload_1
	iconst_5
	if_icmpge Label19
	iconst_1
	goto Label20
Label19:
	iconst_0
Label20:
	ifle Label17
	aload_0
	iload_1
	iaload
	invokestatic io/string_of_int(I)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
Label16:
	iload_1
	iconst_1
	iadd
	istore_1
	goto Label18
Label17:
Label1:
	return
.limit stack 11
.limit locals 4
.end method

.method public <clinit>()V
	return
.limit stack 0
.limit locals 0
.end method

.method public <init>()V
.var 0 is this LMCClass; from Label0 to Label1
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
Label1:
	return
.limit stack 1
.limit locals 1
.end method
