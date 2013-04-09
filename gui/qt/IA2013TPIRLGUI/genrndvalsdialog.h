#ifndef GENRNDVALSDIALOG_H
#define GENRNDVALSDIALOG_H

#include <QDialog>

namespace Ui {
class GenRndValsDialog;
}

class GenRndValsDialog : public QDialog
{
    Q_OBJECT
    
public:
    explicit GenRndValsDialog(QWidget *parent = 0);
    ~GenRndValsDialog();
    
protected:
    void changeEvent(QEvent *e);
    
private:
    Ui::GenRndValsDialog *ui;
};

#endif // GENRNDVALSDIALOG_H
