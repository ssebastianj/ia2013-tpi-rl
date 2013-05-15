#ifndef MATRIZDIALOG_H
#define MATRIZDIALOG_H

#include <QDialog>

namespace Ui {
class MatrizDialog;
}

class MatrizDialog : public QDialog
{
    Q_OBJECT
    
public:
    explicit MatrizDialog(QWidget *parent = 0);
    ~MatrizDialog();
    
protected:
    void changeEvent(QEvent *e);
    
private:
    Ui::MatrizDialog *ui;
};

#endif // MATRIZDIALOG_H
